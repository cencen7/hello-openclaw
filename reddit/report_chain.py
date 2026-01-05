"""
['A,B,C','C,D','B,E']
打印结构tree


A
....B
........E
....C
........D

这是第一部分
第二部分是找skip meeting
比如a和e
a和d
打印出来的形式无所谓，找到这个pair就行
第三部分
找某个人，打印他的上面所有单线manager和下面所有员工
比如说找B
就是
a

....b
........e

第四部分是两个人找最低级别的共同report，
对 c e来说就是a
第一问 打印 report chain
第二问 面试官说他不喜欢， 直接skip了， 上了更难的第三问
第三问 given a name，只打印包含这个人的report chain

写完之后需要当场跑
中间会问复杂度，需要自己想test case
"""
from typing import List, Dict, Set, Optional
from collections import defaultdict



class ReportChain:

    def __init__(self, relations: List[str]) -> None:
        # build children and parent map
        self.children: Dict[str, List[str]] = defaultdict(list)
        self.parent: Dict[str, str] = {}
        self.people: Set[str] = set()

        for relation in relations:
            ppl = [x.strip() for x in relation.split(',')]
            if len(ppl) == 0:
                continue
            manager = ppl[0]
            self.people.add(manager)

            for emp in ppl[1:]:
                self.children[manager].append(emp)
                self.parent[emp] = manager
                self.people.add(emp)

        # find root or roots
        self.roots = [p for p in self.people if p not in self.parent]

    def dfs_print(self, node: str, level: int) -> None:
        print("...." * level + node)
        for child in self.children[node]:
            self.dfs_print(child, level + 1)

    def dfs_skip_print(self, node: str) -> None:
        for child in self.children[node]:
            for grandchild in self.children[child]:
                print(f"Skip pair: {node} and {grandchild}")
            self.dfs_skip_print(child)

    def print_report_chain(self) -> None:
        for root in self.roots:
            self.dfs_print(root, 0)

    def print_skip_chain(self) -> None:
        for root in self.roots:
            self.dfs_skip_print(root)

    def print_person_chain(self, person: str) -> None:
        path = self.get_path_to_root(person)[1:]  # exclude the person themselves
        for level, p in enumerate(path[::-1]):
            print("...." * level + p)
        self.dfs_print(person, level + 1)

    def get_path_to_root(self, person: str) -> List[str]:
        path = []
        while person in self.parent:
            path.append(person)
            person = self.parent[person]
        path.append(person)
        return path

    def find_least_common_report(self, person1: str, person2: str) -> Optional[str]:
        path1 = self.get_path_to_root(person1)
        path2 = self.get_path_to_root(person2)
        for p in path2:
            if p in path1:
                print(f"least common report between {person1} and {person2}: {p}")
                return p
        
        print(f"least common report between {person1} and {person2}: None")
        return None


if __name__ == "__main__":
    data = [ 'F,G', 'A,B,C', 'C,D', 'B,E', 'E,H,I,J,K', "K,Y,W", "Y,Z,9"]
    rc = ReportChain(data)
    rc.print_report_chain()
    rc.print_skip_chain()
    rc.print_person_chain('Y')
    rc.find_least_common_report('9', 'W')