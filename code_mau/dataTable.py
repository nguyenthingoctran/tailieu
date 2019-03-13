===========================================
1. Thêm thư viện:
===========================================
    <link href='{{static ("/vendors/datatables.net-bs4/css/dataTables.bootstrap4.css")}}' rel="stylesheet">

    <script src='{{ static ("/vendors/datatables.net/js/jquery.dataTables.js")}}'></script>
    <script src='{{ static ("/vendors/datatables.net-bs4/js/dataTables.bootstrap4.js")}}'></script>
    <script src='{{ static ("/js/datatables.js")}}'></script>


============================================
2. Tại table trong html thêm thuộc tính id
============================================
    <table id="datatable-coreui" class="table table-striped table-bordered table-hover datatable display nowrap">


============================================
3. Thêm style tùy thích
Lưu ý table phải có div (card-body) bọc ngoài.
============================================
<style>
  div.card-body {
    width: 800px;
	margin: 0 auto;
    }
</style>


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
  "scrollX": true,
  "columnDefs": [ {
    "targets": 'no-sort',
    "orderable": false,
    
  } ]
} );


$('#tbl_data').DataTable( {
  "order": [],
  "bPaginate": true,
  "bLengthChange": false,
  "bFilter": false,
  "bInfo": true,
  "iDisplayLength": 10,
  "columnDefs": [ {
    "targets": 'no-sort',
    "orderable": false,
    
  } ]
} );

Lưu ý:
+ "targets": 'no-sort' ==> tương ứng là class của th đã đặt ở trên

https://stackoverflow.com/questions/17339564/twitter-bootstrap-buttons-appearing-on-hover-over-the-table-row
https://codepen.io/kjohnson/pen/klBzo