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
注意不是optimal cover。
---
https://leetcode.com/discuss/post/897537/facebook-phone-anagram-substring-search-kpaiq/

--
https://leetcode.com/problems/number-of-matching-subsequences/description/ 
"""


class FindSubStr:
    def __init__(self, word):
        self.word = word
        self.chars = list(word.lower())

    def _is_anagram(self, chars1, chars2):
        count = {}
        for c in chars1:
            count[c] = count.get(c, 0) + 1
        for c in chars2:
            if count.get(c, 0) == 0:
                return False
            count[c] -= 1
        return True

    def find_substr(self, substr):
        if len(substr) == 0:
            return 0
        
        if len(substr) > len(self.word):
            return -1
        
        substr_chars = list(substr.lower())
        for i in range(0, len(self.word) - len(substr) + 1):
            tmp = self.chars[i:i+len(substr)]
            if self._is_anagram(tmp, substr_chars):
                return i
            
        return -1
    
if __name__ == "__main__":
    fs = FindSubStr("databricks")
    print(fs.find_substr("tad"))  # 0
    print(fs.find_substr("ribkc"))  # 4
    print(fs.find_substr("abc"))  # -1
    print(fs.find_substr("data"))  # 0
    print(fs.find_substr(""))  # 0
    print(fs.find_substr("databricksx"))  # -1
        
        
       

