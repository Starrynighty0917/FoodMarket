from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    # 这两条一起配置的,下面就是指定用户能不能通过浏览器上的控件指定page_size,可以设置为None
    # http://127.0.0.1:8000/goods/?p=3 => http://127.0.0.1:8000/goods/?p=3&page_size=10以此来修改页面显示数
    page_size = 12
    # 一页有多少个，可以（？p=2&page_size=20）一页有20个
    page_size_query_param = 'page_size'
    max_page_size = 12
    # 将浏览器上的url查询参数名字改为p(?p=2)
    page_query_param = 'page'
