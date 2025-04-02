import psutil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import os


class SystemMonitorView(APIView):
    """
    获取系统资源使用情况的API视图
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 获取内存使用情况
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 获取所有磁盘分区的使用情况
        disks = {}
        for partition in psutil.disk_partitions(all=False):
            # 只处理固定磁盘，跳过CD-ROM等可移动设备
            if os.name == 'nt':
                if 'cdrom' in partition.opts or partition.fstype == '':
                    continue
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                # 使用盘符作为键名（Windows下如C:, D:等）
                drive_letter = os.path.splitdrive(partition.mountpoint)[0]
                if not drive_letter:
                    drive_letter = partition.mountpoint
                disks[drive_letter] = {
                    'total': usage.total,
                    'used': usage.used,
                    'percent': usage.percent,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype
                }
            except (PermissionError, FileNotFoundError):
                # 跳过无法访问的分区
                continue
        
        data = {
            'cpu': {
                'percent': cpu_percent,
            },
            'memory': {
                'total': memory.total,
                'used': memory.used,
                'percent': memory_percent,
            },
            'disks': disks
        }
        
        return Response(data)