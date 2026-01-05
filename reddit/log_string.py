"""
给了一个log string，split by newline之后分别是
mod_given_new_access, action, mod_take_action, timestamp

mod_given_new_access -> user_1, user_2
action -> added, removed
mod_take_action -> user_3, user_4
timestamp -> float

主要是support三个function：
1) mod_list constructor -> parse log and store in your data structure
2) can_remove_mod(user_1, user_2) -> check if user_2 can remove user_1 or not (user_2 should became a moderator earlier than user_1)
3) get_mod_list -> list of all moderators

第一问实现上面三个functions
第二问加了一个community的概念，同样三个function但是每个community有自己的mod list
第三问加了一个新的function: demote(user_1) 就是把user_id的等级调低，比如本来的顺序是[user_1, user_2, user_3], 现在变成[user_2, user_1, user_3]


大致给了一个log string，split by newline之后分别是
mod_given_new_access, action, mode_had_access, timestamp

每个level都需要写三个function：
1) mod_list constructor
2) can_remove_mod
3) get_mod_list

第二个level加了一个community的概念，同样需要写出三个function
第三个level需要demote 当前的mod，也就是当前mod得到access的时间往下调


"""