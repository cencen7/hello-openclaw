"""
非题库题，大概是给两个string，第一个是需要被match的字符串，
第二个是query，用来match第一个的substr的，找出match到的substr的第一个字符的下标，
substr的内部顺序可以不同，类似[databricks, tada] -> 0; [databricks, ribkc] -> 4; 
[databricks, abc] -> -1; [data, databricks] -> -1; 同样需要考虑空字符串等edge cases

----
给定一个字符串比如 “databricks”，以及一个query 比如”tad”，找到字符串中第一次出现query的anagram（回文构词）的下标位置。
比如 字符串是databricks，那给定的query不管是”tad”, “atd”还是”dat”，都是要返回下标0，因为dat 是这几个query的anagram.
def anagram_index(lookup_string, query) -> int
anagram_index(‘databricks’, ‘atd’) 应该返回0，如果query改成sk 则应该返回8

---
coding ref string和source string，
找出ref string里面index可以match上source string的所有pair输出，
第二问是，如果delete其中一个char，怎么改变第一问输出的pair，前提是要保持maximum cover，
注意不是optimal cover。第二个coding是BFS找最节约的交通方式in 2D matrix， 
每个grid有cost，每种交通方式不可以互换，比如bike，walk，bus是三种cost，
一但选择了就不可以换成另一种交通，比较基础的BFS
"""