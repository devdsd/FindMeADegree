
function academicperformance() {
  $.ajax({
    url: "http://127.0.0.1:5000/academicperformance",
    contentType: "application/json; charset=utf-8",
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

          $("#cgpa").append(" " + cgpa)
          

          for (let a = 0; a < syandsem.length; a++) {
              if (syandsem[a][1] == 3) {
                $("#content").append('<tr>' + 
                    '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[a][0] + "&emsp;" + " SEM: " + "Summer Sem" + '</strong>' + "(" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ": " + studentprogram + '</span>) </td>' +
                '</tr>');
              } else {
                $("#content").append('<tr>' + 
                  '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[a][0] + "&emsp;" + " SEM: " + syandsem[a][1] + '</strong>' + "(" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ": " + studentprogram + '</span>) </td>' +
                '</tr>');
              }
              
              for(let b=0; b < subjecthistories.length; b++) {
                    if ( (subjecthistories[b][2]==syandsem[a][0]) && (subjecthistories[b][1]==syandsem[a][1]) ) {
                      console.log((subjecthistories[b][2]==syandsem[a][0]) && (subjecthistories[b][1]==syandsem[a][1]));


                                if (subjecthistories[b][4] == '1.0') {

                                    $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +
                                    '<td><span class="badge" style="background-color:#19751A">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>'); 

                                } else if (subjecthistories[b][4] == '1.25') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' + '<td><span class="badge" style="background-color:#4CAF50">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '1.5') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#8BC349">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '1.75') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#CDDC39">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#FFCF4B">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.25') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#F9B32F">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.5') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' + '<td><span class="badge" style="background-color:#F39C12">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.75') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#E67E22">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '3.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#C86400">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] =='5.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#ff0000">' + subjecthistories[b][4] + "0" + '</span>' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');
                                }
                    }
              }

              for (let d=0; d < gpas.length; d++) {
                if ((gpas[d].sy == syandsem[a][0] ) && (gpas[d].sem == syandsem[a][1] )) {
                  $("#content").append('<tr>' +
                                      '<td colspan="2" class="text-right text-danger">' + "GPA " + '</td>' +
                                      '<td class="text-danger">' + gpas[d].gpa + '</td> </tr>');
                }
              }
          }


        }

      
      } else {
          $("#content").html("");
      }
    },
    
    error: function(e) {
        alert("danger! Something went wrong!");
    }
  
  });
}


function studentinformation() {
  $.ajax({
    url: "http://127.0.0.1:5000/studentinformation",
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
          progdesc = resp.data[i].progdesc;
          scholasticstatus = resp.data[i].scholasticstatus;
          cgpa = resp.data[i].cgpa;
          currentgpa = resp.data[i].currentgpa;
          
          $("#studfnameandlname").append(studfirstname + " " + studlastname);
          $("#studmajor").append(studmajor);
          $("#progdesc").append(progdesc);
          
          
          if (studentlevel === 1) {
            $("#instudentlevel").append("<p><small>" + studentlevel + "st year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 2) {
            $("#instudentlevel").append("<p><small>" + studentlevel + "nd year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 3) {
            $("#instudentlevel").append("<p><small>" + studentlevel + "rd year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }

          else if (studentlevel === 4) {
            $("#instudentlevel").append("<p><small>" + studentlevel + "th year" + '<span style="text-transform: uppercase;">' + " " + studmajor + "</span></small></p>");
          }


          $("#scholasticstatus").append(scholasticstatus);
          $("#currentgpa").append(currentgpa);
          $("#cgpa").append(cgpa);


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



function loadacademicperformance() {
  getInfo();
  academicperformance();
}

function loadstudentinfo() {
  getInfo();
  studentinformation();
}