from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限仅允许对象的所有者对其进行编辑
    假设模型实例具有`owner`属性。
    """
    # 设置当校验失败时，发送给用户的信息
    message = 'Delete Fav not allowed.(你没有此操作的权限^-^)'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许GET，HEAD或OPTIONS 请求.
        if request.method in permissions.SAFE_METHODS:
            return True
        usr = obj.user
        # 这是为了防止要删除的收藏中的用户id和request也就是前端传过来登陆的用户不一样，禁止登录的用户删除其他用户的收藏记录的操作
        return obj.user == request.user