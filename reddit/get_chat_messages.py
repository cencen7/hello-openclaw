"""
a function called get_chat_messages (), you pass in e chat message ID, and it returns 5 messages above and below the given chat ID. The 5 messages above and below a single are inclusive of the given chat ID.
Merge the responses from the get_chat_messages () for each ID in the given list. remove duplicates, and return them in order.
你要实现的方法，它是要接受一个id list，返回这些id list获取到的上下文去重排列后的message list，就比如他给你了1 3 5，你每一个id要先通过它给出的方法获得前后5条，这样他们之间肯定有重复部分，但是你要把他们merge起来去重。应该输出 0 1 2 3 4 5 6 7 8 9 10 . 题目提示不能简单地使用 Set进行 去重后 排序，而是要求你思考其他方法来完成任务。
follow up: Message如果支持修改，保存不同版本怎么办
我觉得是给message这个class增加一个当前版本号，并且维护一个历史版本号/内容的列表.

前几周面了Reddit电面，海投的，HR reach out之前都不了解这家公司，了解了以后发现这确实是个不错的公司。但是题是地里从来没见过的。求加米！

这道题的核心任务是实现一个
merge_messages(ids [])

方法，具体要求如下：
获取聊天消息：提供一个聊天消息 ID 列表（已经给出），每个 ID 通过
get_chat_messages(id)

方法（已经实现）获取其前后 5 条消息（包括自身）。
合并结果：将所有 ID 关联的消息合并成一个集合。
去重：如果多个 ID 获取的消息有重复，需要去重。
排序：最终返回的消息需要按照 ID 进行排序。

题目提示不能简单地使用
Set

进行去重后排序，而是要求你思考其他方法来完成任务。
follow up: Message如果支持修改，保存不同版本怎么办
"""