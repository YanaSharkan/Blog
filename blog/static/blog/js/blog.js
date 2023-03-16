$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#contact .modal-content").html("");
        $("#contact").modal("show");
      },
      success: function (data) {
        $("#contact .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#contact").modal("hide");
          setTimeout(function () {
            alert("Feedback Sent!");
          }, 1000);
        }
        else {
          $("#contact .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  $(".js-add-feedback").click(loadForm);
  $("#contact").on("submit", ".js-add-feedback-form", saveForm);

});