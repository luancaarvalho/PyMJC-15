from __future__ import annotations
from abc import abstractmethod
import sys
import queue
from typing import List, Set
from pymjc.back import assem, flowgraph, graph
from pymjc.front import frame, temp


class RegAlloc (temp.TempMap):
    def __init__(self, frame: frame.Frame, instr_list: assem.InstrList):
        self.frame: frame.Frame = frame
        self.instrs: assem.InstrList = instr_list

        self.pre_colored_nodes: Set[graph.Node] = []

        self.initial_nodes: Set[graph.Node] = []
        self.spill_nodes: Set[graph.Node] = []

        self.node_stack: List[graph.Node] = []

        self.simplify_work_list: Set[graph.Node] = []
        self.freeze_work_list: Set[graph.Node] = []
        self.spill_work_list: Set[graph.Node] = []
        
        self.worklist_move_nodes: Set[graph.Node] = []

        self.spill_cost: dict[graph.Node,int] = []

        self.liveness_output: Liveness = {}
        self.assem_flow_graph: flowgraph.AssemFlowGraph = {}

        self.move_nodes_list: dict[graph.Node, Set[graph.Node]] = []

        self.node_degree_table: dict[graph.Node, int] = []
        self.node_color_table: dict[graph.Node, graph.Node] = []

        self.main()

    def main(self):
        should_continue: bool = True
        while(should_continue):
            should_continue = False
            
            self.liveness_analysis()
            self.build()
            self.make_work_list()

            while True:
                if (len(self.simplify_work_list) != 0):
                    self.simplify()
                elif (len(self.worklist_move_nodes) != 0):
                    self.coalesce()
                elif (len(self.freeze_work_list) != 0):
                    self.freeze()
                elif (len(self.spill_work_list) != 0):
                    self.select_spill()

                if not(len(self.simplify_work_list) != 0 or len(self.worklist_move_nodes) != 0 or len(self.freeze_work_list) != 0 or len(self.spill_work_list) != 0):
                    break

            self.assign_colors()

            if (len(self.spill_nodes) != 0):
                self.rewrite_program() 
                should_continue = True

    def liveness_analysis(self):
        self.assem_flow_graph = flowgraph.AssemFlowGraph(self.instrs)

        self.liveness_output = Liveness(self.assem_flow_graph)

    def build(self):
        node_list: graph.NodeList = self.assem_flow_graph.nodes()

        while(node_list is not None):
            node: graph.Node = node_list.head

            live: set[temp.Temp] = self.liveness_output.out(node)

            is_move_instruction: bool = self.assem_flow_graph.is_move(node)
            if (is_move_instruction):
                uses: temp.TempList = self.assem_flow_graph.use(node)

                while(uses is not None):
                    live.remove(uses.head)
                    uses = uses.tail

                uses: temp.TempList = self.assem_flow_graph.use(node)

                while(uses is not None):
                    self.move_nodes_list(self.liveness_output.tnode(uses.head))[node] = node
                    uses = uses.tail

                self.worklist_move_nodes.add(node)

            defs: temp.TempList = self.assem_flow_graph.deff(node)

            while(defs is not None):
                live.add(defs.head)  
                defs = defs.tail  

            defs: temp.TempList = self.assem_flow_graph.deff(node)

            while(defs is not None):
                for live_temp in live:
                    self.add_edge(live_temp, defs.head)
                defs = defs.tail 

            node_list = node_list.tail

    def make_work_list(self):
        K: int = len(self.pre_colored_nodes)

        node_iterator = iter(self.initial_nodes)

        while(next(node_iterator, None) is not None):
            node: graph.Node = next(node_iterator)

            self.initial_nodes.remove(node_iterator)  

            if(self.node_degree_table(node) >= K):
                self.spill_work_list.add(node)
            elif(self.move_related(node)):
                self.freeze_work_list.add(node)
            else:
                self.simplify_work_list.add(node)     

    def simplify(self):
        temporary_iterator = iter(self.simplify_work_list)
        node: graph.Node = next(temporary_iterator)

        self.simplify_work_list.remove(temporary_iterator)

        self.node_stack.append(node)

        for no in node.adj:
            self.decrement_degree(no)

    def coalesce(self):
        pass

    def conservative(self,nodes:Set[graph.Node]):
        k: int = 0
        K: int = len(self.pre_colored_nodes)

        for node in nodes:
            if (self.node_degree_table.get(node)>=K):
                k += 1

        return k<K

    def temp_map(self, temp: temp.Temp) -> str:
        str = self.frame.temp_map(temp)

        if(str is None):
            str = self.frame.temp_map(self.liveness_output.gtemp(self.node_color_table.get(self.liveness_output.tnode(temp))))

        return temp.to_string()


class Color(temp.TempMap):
    def __init__(self, ig: InterferenceGraph, initial: temp.TempMap, registers: temp.TempList):
        #TODO
        pass
    
    def spills(self) -> temp.TempList:
        #TODO
        return None

    def temp_map(self, temp: temp.Temp) -> str:
        #TODO
        return temp.to_string()

class InterferenceGraph(graph.Graph):
    
    @abstractmethod
    def tnode(self, temp:temp.Temp) -> graph.Node:
        pass

    @abstractmethod
    def gtemp(self, node: graph.Node) -> temp.Temp:
        pass

    @abstractmethod
    def moves(self) -> MoveList:
        pass
    
    def spill_cost(self, node: graph.Node) -> int:
      return 1


class Liveness (InterferenceGraph):

    def __init__(self, flow: flowgraph.FlowGraph):
        self.live_map = {}
        
        #Flow Graph
        self.flowgraph: flowgraph.FlowGraph = flow
        
        #IN, OUT, GEN, and KILL map tables
        #The table maps complies with: <Node, Set[Temp]>
        self.in_node_table = {}
        self.out_node_table = {}
        self.gen_node_table = {}
        self.kill_node_table = {}

        #Util map tables
        #<Node, Temp>
        self.rev_node_table = {}
        #<Temp, Node>
        self.map_node_table = {}
        
        #Move list
        self.move_list: MoveList = None

        self.build_gen_and_kill()
        self.build_in_and_out()
        self.build_interference_graph()
    
    def add_ndge(self, source_node: graph.Node, destiny_node: graph.Node):
        if (source_node is not destiny_node and not destiny_node.comes_from(source_node) and not source_node.comes_from(destiny_node)):
            super.add_edge(source_node, destiny_node)

    def show(self, out_path: str) -> None:
        if out_path is not None:
            sys.stdout = open(out_path, 'w')   
        node_list: graph.NodeList = self.nodes()
        while(node_list is not None):
            temp: temp.Temp = self.rev_node_table.get(node_list.head)
            print(temp + ": [ ")
            adjs: graph.NodeList = node_list.head.adj()
            while(adjs is not None):
                print(self.rev_node_table.get(adjs.head) + " ")
                adjs = adjs.tail

            print("]")
            node_list = node_list.tail
    
    def get_node(self, temp: temp.Temp) -> graph.Node:
      requested_node: graph.Node = self.map_node_table.get(temp)
      if (requested_node is None):
          requested_node = self.new_node()
          self.map_node_table[temp] = requested_node
          self.rev_node_table[requested_node] = temp

      return requested_node

    def node_handler(self, node: graph.Node):
        def_temp_list: temp.TempList = self.flowgraph.deff(node)
        while(def_temp_list is not None):
            got_node: graph.Node  = self.get_node(def_temp_list.head)

            for live_out in self.out_node_table.get(node):
                current_live_out = self.get_node(live_out)
                self.add_edge(got_node, current_live_out)

            def_temp_list = def_temp_list.tail

  
    def move_handler(self, node: graph.Node):
        source_node: graph.Node  = self.get_node(self.flowgraph.use(node).head)
        destiny_node: graph.Node = self.get_node(self.flowgraph.deff(node).head)

        self.move_list = MoveList(source_node, destiny_node, self.move_list)
    
        for temp in self.out_node_table.get(node):
            got_node: graph.Node = self.get_node(temp)
            if (got_node is not source_node ):
                self.addEdge(destiny_node, got_node)


    def out(self, node: graph.Node) -> Set[temp.Temp]:
        temp_set = self.out_node_table.get(node)
        return temp_set


    def tnode(self, temp:temp.Temp) -> graph.Node:
        node: graph.Node = self.map_node_table.get(temp)
        if (node is None ):
            node = self.new_node()
            self.map_node_table[temp] = node
            self.rev_node_table[node] = temp
        
        return node

    def gtemp(self, node: graph.Node) -> temp.Temp:
        temp: temp.Temp = self.rev_node_table.get(node)
        return temp

    def moves(self) -> MoveList:
        return self.move_list

    def build_gen_and_kill(self):
        node_list: graph.NodeList = self.flowgraph.nodes()
        while(node_list.head is not None):
            node_list = node_list.tail

            temp_gen: Set[graph.Node] = []
            aux_gen: temp.TempList = self.flowgraph.use(node_list.head)
            while(aux_gen is not None):
                temp_gen.add(aux_gen.head)
                aux_gen = aux_gen.tail

            temp_kill: Set[graph.Node] = []
            aux_kill: temp.TempList = self.flowgraph.use(node_list.head)
            while(aux_kill is not None):
                temp_kill.add(aux_kill.head)
                aux_kill = aux_kill.tail

            self.kill_node_table[node_list.head] = temp_kill
            self.gen_node_table[node_list.head] = temp_gen

    def build_in_and_out(self):
        node_list: graph.NodeList = self.flowgraph.nodes()
        while(node_list.head is not None):
            self.in_node_table[node_list.head] = Set[temp.Temp]
            self.out_node_table[node_list.head] = Set[temp.Temp]

            node_list = node_list.tail

        finished: bool = False
        while(not finished):
            node_list: graph.NodeList = self.flowgraph.nodes()
            while(node_list.head is not None):
                temp_in_set: Set(temp.Temp) = self.in_node_table[node_list.head]
                temp_out_set: Set(temp.Temp) = self.out_node_table[node_list.head]

                node_list_succ: graph.NodeList = node_list.head.succ()
                while(node_list_succ.head is not None):
                    self.out_node_table[node_list_succ.head] = self.in_node_table[node_list_succ.head]
                    node_list_succ = node_list_succ.tail

                self.out_node_table[node_list.head] = {}
                self.gen_node_table[node_list.head] = {}
                self.in_node_table[node_list.head] = {}

                finished = ((not all(elem in temp_in_set for elem in self.in_node_table[node_list.head]))
                            or (not all(elem in temp_out_set for elem in self.out_node_table[node_list.head])))

                node_list=node_list.tail

    def build_interference_graph(self):
        node_list: graph.NodeList = self.flowgraph.nodes()

        while(node_list.head is not None):
            if (self.flowgraph.is_move(node_list.head)):
                self.move_handler(node_list.head())
            else:
                self.node_handler(node_list.head())
            node_list = node_list.tail

class Edge():

    edges_table = {}

    def __init__(self):
        super.__init__()
    
    def get_edge(self, origin_node: graph.Node, destiny_node: graph.Node) -> Edge:
        
        origin_table = Edge.edges_table.get(origin_node)
        destiny_table = Edge.edges_table.get(destiny_node)
        
        if (origin_table is None):
            origin_table = {}
            Edge.edges_table[origin_node] = origin_table

        if (destiny_table is None):
            destiny_table = {}
            Edge.edges_table[destiny_node] = destiny_table
        
        requested_edge: Edge  = origin_table.get(destiny_node)

        if(requested_edge is None):
            requested_edge = Edge()
            origin_table[destiny_node] = requested_edge
            destiny_table[origin_node] = requested_edge

        return requested_edge



class MoveList():

   def __init__(self, s: graph.Node, d: graph.Node, t: MoveList):
      self.src: graph.Node = s
      self.dst: graph.Node = d
      self.tail: MoveList = t
