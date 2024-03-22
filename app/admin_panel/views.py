from django.shortcuts import render,redirect
from .models import AdminUser, ModelInfo
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from model.model import train
from sklearn.metrics import ConfusionMatrixDisplay  

import matplotlib.pyplot as plt
import seaborn as sns

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Received username:", username)
        print("Received password:", password)

        admin = authenticate(request, username=username, password=password)
        if admin is not None:
            login(request, admin)
            print("Authentication successful")
            return redirect('admin')
        else:
            error_message = "Invalid username or password"
            print("Authentication failed")
            return render(request, 'admin_login.html', {'error_message': error_message})
    else:
        return render(request, 'admin_login.html')

         
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_dashboard(request):
      return render(request, 'admin_dashboard.html')

@login_required
def admin_model(request):
    ai_model = ModelInfo.objects.all()
    model_info = ai_model[0]

    acc = []

    if model_info.old_acc == -1:
        acc.append("N/A")

    else:
        acc.append(round(model_info.old_acc, 5))

    return render(request, 'admin_model.html', {
        "conf_mat": model_info.conf_matrix,
        "train_time": model_info.training_time,
        "old_acc": acc[0],
        "accuracy": model_info.accuracy,
        "precision": model_info.precision,
        "recall": model_info.recall,
        "f_one": model_info.f_one
    })

@login_required
def admin_reports(request):
      return render(request, 'admin_reports.html')

@login_required
@csrf_protect
def admin_admins(request):
    if request.method == 'POST':
        if 'create_admin' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            try:
                AdminUser.objects.create_user(username=username, password=password, email=email)
                return redirect('admin_admins')
            except Exception as e:
                print(f"Error creating admin user: {e}")
        elif 'delete_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            AdminUser.objects.filter(id=admin_id).delete()
            return redirect('admin_admins')
    admin_users = AdminUser.objects.all()
    return render(request, 'admin_admins.html', {'admin_users': admin_users})

@login_required
def retrain(user):
    cf_loc = "admin_panel/static/conf_mat.png"
    training_time, score, conf_mat, recall, prec, acc, f_one = train()
    ai_model = ModelInfo.objects.all()

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    sns.heatmap(conf_mat, cmap='Blues',
                fmt='', annot=True, cbar=False,
                annot_kws={'fontsize': 10, 'fontweight': 'bold'},
                square=False)

    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(cf_loc)

    if len(ai_model) == 0:
        model = ModelInfo(
            conf_matrix = cf_loc,
            training_time = training_time,
            old_acc = -1,
            accuracy = acc,
            precision = prec,
            recall = recall,
            f_one = f_one
        )

        model.save()

    else:
        ai_model[0].training_time = training_time
        ai_model[0].old_acc = ai_model[0].accuracy
        ai_model[0].accuracy = acc
        ai_model[0].precision = prec
        ai_model[0].recall = recall
        ai_model[0].f_one = f_one

        ai_model[0].save()

    return redirect("/admin/model")