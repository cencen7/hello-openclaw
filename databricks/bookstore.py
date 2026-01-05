"""
Bookseller platform 地里原题 这里补充一些细节 
1）这是一个async的请求 关注点不在于如何快速返回请求而是如何不overload downstream API provider
 2）需要自己设计downstream provider的API 
 3）这些provider也会有其他方式卖书 所以要考虑如果书在query price后卖掉了导致无法hold 
 所以不能只找到最便宜的 要按价钱排序 然后按顺序发hold request 
 4）不用考虑数量问题
"""