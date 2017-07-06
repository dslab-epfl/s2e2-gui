import os
import shutil

from django.http import HttpResponse
from django.shortcuts import render

from display_all_analysis.models import Analysis
import s2e_web.S2E_settings as settings
from configure_and_run_analysis.views import displayAnalysisInDir


def handleRequest(request):
    """
    Handle the requests from the display_all_analysis page.
    """
    if request.method == 'GET':
        return render(request, 'display_all_analysis/index.html',
                      {"analysis" : group_by(Analysis.objects.all(), lambda x: x.binary_name)})
    elif request.method == 'POST':
        if request.POST["method"] == "display":
            s2e_num = request.POST["s2e_num"]
            binary_name = request.POST["binary_name"]

            return displayAnalysisInDir(request, s2e_num, binary_name)
        elif request.POST["method"] == "remove":
            s2e_num = request.POST["s2e_num"]
            binary_name = request.POST["binary_name"]

            Analysis.objects.filter(binary_name=binary_name, s2e_num=s2e_num).delete()

            s2e_output_dir_to_delete = os.path.join(settings.S2E_PROJECT_FOLDER_PATH, binary_name,
                                                    's2e-out-%d' % s2e_num)
            shutil.rmtree(s2e_output_dir_to_delete)

            return HttpResponse(status=200)


def group_by(data_list, func):
    output = {}

    for data in data_list:
        key = func(data)
        if not key in output:
            output[key] = [data]
        else:
            output[key].append(data)

    return output
