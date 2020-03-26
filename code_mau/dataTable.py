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

============================================
================ DataTable =================
============================================
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
  "aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
  "bPaginate": true,
  "bLengthChange": false,
  "bFilter": false,
  "bInfo": true,
  "iDisplayLength": 10,
  "columnDefs": [ {
    "targets": 'no-sort',
    "orderable": false,
    "ordering": false // Xóa hoàn toàn các order sort
  } ]
} );

Lưu ý:
+ "targets": 'no-sort' ==> tương ứng là class của th đã đặt ở trên

=======================================================
========== Lỗi table không full hết trang =============
=======================================================
$('#example').dataTable( {
    "autoWidth": false
});

https://stackoverflow.com/questions/17339564/twitter-bootstrap-buttons-appearing-on-hover-over-the-table-row
https://codepen.io/kjohnson/pen/klBzo


=======================================================
===================== Fixed header ====================
=======================================================
link
  <link href='https://cdn.datatables.net/fixedheader/3.1.5/css/fixedHeader.bootstrap4.min.css' rel="stylesheet">
  <script src='https://cdn.datatables.net/fixedheader/3.1.5/js/dataTables.fixedHeader.min.js'></script>

  fixedHeader: {
      header: true,
      headerOffset: $('#fixed').height() # #fixed: là id của div header hiển thị
  }

# ===============================================================================
# =============================== TABLE MẪU =====================================
# ===============================================================================

<table class="table table-responsive-sm table-hover table-sm" >
  <thead>
    <th>DATE ISSUED</th>
    <th>INVOICE CODE</th>
    <th>INVOICE TIME</th>
    <th>PAYMENT ACCOUNT</th>
    <th>STATUS</th>
  </thead>
  <tbody>
    <tr>
      <td class="position-relative">
        <span>2019-04-21</span>
        <!-- Button action -->
        <div class="button-action position-absolute py-0" style="top:2px; right: 30px; background: #ececec;">
          <!-- Button download -->
          <a href="#" class="btn-sm btn-secondary font-weight-bold" 
                      style="box-shadow: 1px 1px 1px #7f8c8d" 
                      title="Edit">
            Download
          </a>
          </div>       
      </td>
      <td>639256</td>
      <td>2019/03/22 - 2019/04/21</td>
      <td>$58,000</td>
      <td>Paid</td>
    </tr>
  </tbody>
</table>

<script type="text/javascript">
// JS cho phần hiện, ẩn các nút action khi hover vào từng dòng của table
hover_table_show_button();
</script>


=========================================================
===================== scroll ============================
=========================================================
<table id="datatable-coreui" class="table table-striped table-bordered table-hover datatable display nowrap">

$('#datatable-coreui').DataTable( {
  "order": [],
  "scrollX": true,
  "columnDefs": [ {
    "targets": 'no-sort',
    "orderable": false,
  } ]
} );

=========================================================
===============-====== next trang =======================
=========================================================
Khi next trang không chạy popover thi chạy lại poperver trong hàm này

  $('#table_cta').on('draw.dt', function () {
      show_popover();
      console.log("draw")
  });