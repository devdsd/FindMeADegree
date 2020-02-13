function getInfo() {
  $.ajax({
    url: "http://127.0.0.1:5000/home",
    contentType: "application/json",
    type: "GET",
    dataType: "json",

    success: function(resp) {
      if (resp.status == "ok") {
        for (i = 0; i < resp.count; i++) {
          studfirstname = resp.data[i].studfirstname;
          studlastname = resp.data[i].studlastname;
          studentlevel = resp.data[i].studentlevel;
          studmajor = resp.data[i].studmajor;
          
          $("#studname").append(studfirstname);
          $("#studname2").append(studfirstname);
          

          $("#firstandlastname").append(studfirstname+ " " +studlastname);
          
          if (studentlevel === 1) {
            $("#studentlevel").append("<p><small>" + studentlevel + "st year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 2) {
            $("#studentlevel").append("<p><small>" + studentlevel + "nd year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 3) {
            $("#studentlevel").append("<p><small>" + studentlevel + "rd year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 4) {
            $("#studlevel").append("<p><small>" + studentlevel + "th year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }
      }

      } else {
        alert("Sorry");
      }
    },

    error: function(e) {
      alert("danger! Something went wrong!");
    }
  });
}


function academicperformance() {
  $.ajax({
    url: "http://127.0.0.1:5000/academic_performance",
    contentType: "application/json",
    type: "GET",
    dataType: "json",

    success: function(resp) {
      if (resp.status == "ok") {
        for (i = 0; i < resp.count; i++) {
          studentlevel = resp.data[i].studentlevel;
          cgpa = resp.data[i].cgpa;
          syandsem = resp.data[i].syandsem;
          studmajor = resp.data[i].studmajor;
          studentprogram = resp.data[i].studentprogram;
          subjecthistories = resp.data[i].subjecthistories;
          gpas = resp.data[i].gpas;

          
          $("#academicperformance").append(
            '<div class="box">' + 
              '<div class="table-responsive">' +
                  '<div class="box-" style="padding: 15px;">' +
                      '<p> <strong>' + "Cummulative GPA: " + '<span style="color: red;">' + cgpa + '</span> </strong> </p>' +

                      '<table class="table table-bordered table-hover table-striped">' + 
                          '<tbody>' + 
                              '<tr class="active">' +
                                  '<th width="3%">' + "SubjCode" + '</th>' +
                                  '<th width="25%">' + "Description" + '</th>' +
                                  '<th width="5%">' + "Grade" + '</th>' +
                              '</tr>'
            );

            for (let i = 0; i < syandsem.length; i++) {
                if (syandsem[i].sem == 3) {
                  $("#academicperformance").append('<tr>' + 
                      '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[i].sy + "SEM: " + "Summer Sem" + '</strong>' + "(" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ":" + studentprogram + '</span>) </td>' +
                  '</tr>');
                } else {
                  $("#academicperformance").append('<tr>' + 
                    '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[i].sy + "SEM: " + syandsem[i].sem + '</strong>' + "(" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ":" + studentprogram + '</span>) </td>' +
                  '</tr>');
                }
                
                for(let i=0; i < subjecthistories.length; i++) {
                      if ((subjecthistories[i].sy == syandsem[i].sy) && (subjecthistories[i].sem == syandsem[i].sem)) {
                        $("#academicperformance").append('<tr>' +
                                  '<td>' + subjecthistories[i].subjcode + '</td>' +
                                  '<td>' + subjecthistories[i].subjdesc + '</td>');

                                  if (subjecthistories[i].grade == '1.0') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#19751A">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>'); 

                                  } else if (subjecthistories[i].grade == '1.25') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#4CAF50">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '1.5') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#8BC349">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '1.75') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#CDDC39">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '2.0') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#FFCF4B">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '2.25') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#F9B32F">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '2.5') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#F39C12">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '2.75') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#E67E22">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade == '3.0') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#C86400">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                  } else if (subjecthistories[i].grade =='5.0') {
                                    $("#academicperformance").append('<td><span class="badge" style="background-color:#ff0000">' + subjecthistories[i].grade + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');
                                  }
                      }
                      
                }

                for (let i=0; gpas.length; i++) {
                  if (gpas[i].sy == syandsem[i].sy ) and (gpas[i].sem == syandsem[i].sem ) {
                    $("#academicperformance").append('<tr>' +
                                        '<td colspan="2" class="text-right text-danger">' + "GPA " + '</td>' +
                                        '<td class="text-danger">' + gpas[i].gpa + '</td>' +
                                      '</tr> </tbody> </table> </div> </div> </div>');
                  }
                }
            }


            }

        } else {
          $("#academicperformance").html("");
      }
    },
    
    error: function(e) {
        alert("danger! Something went wrong!");
    }
  
  });
}