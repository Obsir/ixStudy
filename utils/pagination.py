# 优化分页器url，保留原始get参数
class Pagination:
    def __init__(self, request, length, per_num=10, max_show=11, clazz='pager'):
        try:
            page = int(request.GET.get('page', 1))
            if page <= 0:
                page = 1
        except Exception:
            page = 1


        qd = request.GET.copy()
        # 总页码数
        total_num, more = divmod(length, per_num)
        if more:
            total_num += 1
        if page >= total_num:
            page = total_num
        half_show = max_show // 2
        # 页码起始值
        if total_num <= max_show:
            page_start = 1
            page_end = total_num
        else:
            # 处理左边的极值
            if page - half_show <= 0:
                page_start = 1
                page_end = max_show
            elif page + half_show >= total_num:
                page_start = total_num - max_show + 1
                page_end = total_num
            else:
                page_start = page - half_show
                page_end = page + half_show

        page_list = ['<nav aria-label="Page navigation"><ul class="{}">'.format(clazz)]

        if page == 1:
            page_list.append(
                '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            qd['page'] = page - 1
            page_list.append(
                '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    qd.urlencode()))

        for i in range(page_start, page_end + 1):
            qd['page'] = i
            if i == page:
                page_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(qd.urlencode(), i))
            else:
                page_list.append('<li><a href="?{}">{}</a></li>'.format(qd.urlencode(), i))

        if page == total_num:
            page_list.append(
                '<li class="disabled"><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            qd['page'] = page + 1
            page_list.append(
                '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    qd.urlencode()))
        page_list.append('</ul></nav>')
        self.page_html = ''.join(page_list)
        # 切片起始值
        self.start = (page - 1) * per_num
        # 切片终止值
        self.end = page * per_num
        if length < 1:
            self.start = 0
            self.end = 0
