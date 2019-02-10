===========================================
1. Thêm thư viện:
===========================================

  <head>
    <base href="./">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <meta name="description" content="CoreUI - Open Source Bootstrap Admin Template">
    <meta name="author" content="Łukasz Holeczek">
    <meta name="keyword" content="Bootstrap,Admin,Template,Open,Source,jQuery,CSS,HTML,RWD,Dashboard">
    <title>{% block title %}{% endblock  %}</title>
    <!-- Icons-->
    <link href='{{ static ("/vendors/@coreui/icons/css/coreui-icons.min.css") }}' rel="stylesheet">
    <link href='{{ static ("/vendors/flag-icon-css/css/flag-icon.min.css") }}' rel="stylesheet">
    <link href='{{ static ("/vendors/font-awesome/css/font-awesome.min.css") }}' rel="stylesheet">
    <link href='{{ static ("/vendors/simple-line-icons/css/simple-line-icons.css") }}' rel="stylesheet">
    <!-- Main styles for this application-->
    <link href='{{ static ("/css/style.css")}}' rel="stylesheet">
    <link href='{{static ("/vendors/pace-progress/css/pace.min.css")}}' rel="stylesheet">
    <link href='{{static ("/vendors/datatables.net-bs4/css/dataTables.bootstrap4.css")}}' rel="stylesheet">
    {% block linkStyle %}{% endblock  %}
    <!-- CSS STYLES -->
    <style>{% block style %}{% endblock  %}</style>
    <!-- CoreUI and necessary plugins-->
    <script src='{{ static ("/vendors/jquery/js/jquery.min.js")}}'></script>
    <script src='{{ static ("/vendors/popper.js/js/popper.min.js")}}'></script>
    <script src='{{ static ("/vendors/bootstrap/js/bootstrap.min.js")}}'></script>
    <script src='{{ static ("/vendors/pace-progress/js/pace.min.js") }}'></script>
    <script src='{{ static ("/vendors/perfect-scrollbar/js/perfect-scrollbar.min.js")}}'></script>
    <script src='{{ static ("/vendors/@coreui/coreui-pro/js/coreui.min.js") }}'></script>
    <!-- Plugins and scripts required by this view-->
    <script src='{{ static ("/vendors/datatables.net/js/jquery.dataTables.js")}}'></script>
    <script src='{{ static ("/vendors/datatables.net-bs4/js/dataTables.bootstrap4.js")}}'></script>
    <script src='{{ static ("/js/datatables.js")}}'></script>
    <script src='{{ static ("/vendors/chart.js/js/Chart.min.js")}}'></script>
    <script src='{{ static ("/vendors/@coreui/coreui-plugin-chartjs-custom-tooltips/js/custom-tooltips.min.js") }}'></script>
    <script src='{{ static ("/js/main.js") }}'></script>
    <!-- Global site tag (gtag.js) - Google Analytics-->
    <script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-118965717-3"></script>
    
  </head>


============================================
2. Tạo table trong html
============================================
        <div class="container-fluid">
          <div class="animated fadeIn">
            <div class="card">
              <div class="card-header">
                <i class="fa fa-edit"></i> DataTables
                <div class="card-header-actions">
                  <a class="card-header-action" href="https://datatables.net" target="_blank">
                    <small class="text-muted">docs</small>
                  </a>
                </div>
              </div>
              <div class="card-body">
                <table id="datatable-coreui" class="table table-striped table-bordered datatable">
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Date registered</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Anton Phunihel</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Alphonse Ivo</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Thancmar Theophanes</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Walerian Khwaja</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Clemens Janko</td>
                      <td>2012/02/01</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Chidubem Gottlob</td>
                      <td>2012/02/01</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Hristofor Sergio</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Tadhg Griogair</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Pollux Beaumont</td>
                      <td>2012/01/21</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Adam Alister</td>
                      <td>2012/01/21</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Carlito Roffe</td>
                      <td>2012/08/23</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Sana Amrin</td>
                      <td>2012/08/23</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Adinah Ralph</td>
                      <td>2012/06/01</td>
                      <td>Admin</td>
                      <td>
                        <span class="badge badge-dark">Inactive</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Dederick Mihail</td>
                      <td>2012/06/01</td>
                      <td>Admin</td>
                      <td>
                        <span class="badge badge-dark">Inactive</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Hipólito András</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Fricis Arieh</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Scottie Maximilian</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Bao Gaspar</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Tullio Luka</td>
                      <td>2012/02/01</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Felice Arseniy</td>
                      <td>2012/02/01</td>
                      <td>Admin</td>
                      <td>
                        <span class="badge badge-dark">Inactive</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Finlay Alf</td>
                      <td>2012/02/01</td>
                      <td>Admin</td>
                      <td>
                        <span class="badge badge-dark">Inactive</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Theophilus Nala</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Sullivan Robert</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Kristóf Filiberto</td>
                      <td>2012/01/21</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Kuzma Edvard</td>
                      <td>2012/01/21</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-success">Active</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Bünyamin Kasper</td>
                      <td>2012/08/23</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Crofton Arran</td>
                      <td>2012/08/23</td>
                      <td>Staff</td>
                      <td>
                        <span class="badge badge-danger">Banned</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Bernhard Shelah</td>
                      <td>2012/06/01</td>
                      <td>Admin</td>
                      <td>
                        <span class="badge badge-dark">Inactive</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Grahame Miodrag</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Innokentiy Celio</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Kostandin Warinhari</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>Ajith Hristijan</td>
                      <td>2012/03/01</td>
                      <td>Member</td>
                      <td>
                        <span class="badge badge-warning">Pending</span>
                      </td>
                      <td>
                        <a class="btn btn-success" href="#">
                          <i class="fa fa-search-plus"></i>
                        </a>
                        <a class="btn btn-info" href="#">
                          <i class="fa fa-edit"></i>
                        </a>
                        <a class="btn btn-danger" href="#">
                          <i class="fa fa-trash-o"></i>
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>


============================================
3. Thêm style tùy thích
Lưu ý table phải có div bọc ngoài.
============================================
<style>
  div.card-body {
    width: 800px;
	margin: 0 auto;
    }
</style>


============================================
4. Thêm javascript
============================================
  $(document).ready(function() {
      $('#datatable-coreui').DataTable( {

      } );

  } );



*********************************************************************************************************************************
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
*********************************************************************************************************************************

============================================
5. BỎ SẮP XẾP THEO CỘT TÙY CHỌN
============================================
5.1 Thêm class vào th muốn bỏ icon sx
     <th class="no-sort" class="checkAll"><input id="checkAll" type="checkbox" value=""></th>

5.2 Js
  $('#datatable-coreui').DataTable( {
    "order": [],
    "columnDefs": [ {
      "targets": 'no-sort',
      "orderable": false,
      
    } ]
  } );

  Lưu ý:
  + "targets": 'no-sort' ==> tương ứng là class của input đã đặt ở trên