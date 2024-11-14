from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from video_manager.forms import VideoSearchForm, VideoForm
from video_manager.models import Video

# Create your views here.
def video_list(request):
    search_form = VideoSearchForm(request.GET or None)
    query = search_form.data.get("query", "")
    videos = Video.objects.filter(title__icontains=query)

    return render(request, "video_manager/video_list.html", {
        "videos": videos,
        "search_form": search_form,
        "query": query,
        "user": request.user,
    })

def video_detail(request, pk):
    videos = Video.objects.all()
    video = get_object_or_404(Video, pk=pk)
    return render(request, "video_manager/video_detail.html", {
        "video": video, "videos": videos.order_by('-id')[:5],
    })

@login_required
def create_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect("video_list")
    else:
        form = VideoForm()
    return render(request, "video_manager/video_form.html", {
        "form": form,
    })

@login_required
def update_video(request, pk):
    video = get_object_or_404(Video, pk=pk, user=request.user)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect("video_list")
    else:
        form = VideoForm(instance=video)
    return render(request, "video_manager/video_form.html", {
        "form": form,
    })

@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk, user=request.user)
    if request.method == "POST":
        video.delete()
        return redirect("video_list")
    return render(request, "video_manager/video_confirm_delete.html", {
        "video": video,
    })