function home() {
  var varstudid = document.getElementsByClassName('bodyclass')[0].id;
  $.ajax({
    url: "http://127.0.0.1:5000/home",
    contentType: "application/json",
    type: "GET",
    dataType: "json",
    async: false,
    data: { "studid": String(varstudid) },

    success: function(resp) {

      if (resp.status == "ok") {
        for (i = 0; i < resp.count; i++) {

          studidval = resp.data[i].studid;
          studfirstname = resp.data[i].studfirstname;
          studlastname = resp.data[i].studlastname;
          studentlevel = resp.data[i].studentlevel;
          studmajor = resp.data[i].studmajor;
          
          globaltemplate(studfirstname, studlastname, studentlevel, studmajor);

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



function globaltemplate(studfirstname, studlastname, studentlevel, studmajor) {

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



function studentinformation() {
  var varstudid = document.getElementsByClassName('bodyclass')[0].id;
  $.ajax({
    url: "http://127.0.0.1:5000/student_information",
    contentType: "application/json",
    type: "GET",
    dataType: "json",
    async: false,
    data: { "studid": String(varstudid) },

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

          globaltemplate(studfirstname, studlastname, studentlevel, studmajor);
          
          $("#studfnameandlname").append(studfirstname + " " + studlastname);
          $("#studmajor").append('(' + studmajor + ')');
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


          $("#scholasticstatus").append('<strong>'+scholasticstatus+'</strong>');
          $("#currentgpa").append('<strong>'+currentgpa+'</strong>');
          $("#cgpa").append('<strong>'+cgpa+'</strong>');


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
  var varstudid = document.getElementsByClassName('bodyclass')[0].id;
  $.ajax({
    url: "http://127.0.0.1:5000/academic_performance",
    contentType: "application/json; charset=utf-8",
    type: "GET",
    dataType: "json",
    async: false,
    data: { "studid": String(varstudid) },

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
                    '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[a][0] + "&emsp;" + " SEM: " + "Summer Sem" + '</strong>' + " (" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ": " + studentprogram + '</span>) </td>' +
                '</tr>');
              } else {
                $("#content").append('<tr>' + 
                  '<td colspan="3" class="danger"> <strong>' + "SY:  " + syandsem[a][0] + "&emsp;" + " SEM: " + syandsem[a][1] + '</strong>' + " (" + '<span class="text-muted" style="text-transform: uppercase;">' + studmajor + ": " + studentprogram + '</span>) </td>' +
                '</tr>');
              }
              
              for(let b=0; b < subjecthistories.length; b++) {
                    if ( (subjecthistories[b][2]==syandsem[a][0]) && (subjecthistories[b][1]==syandsem[a][1]) ) {

                                if (subjecthistories[b][4] == '1.0') {

                                    $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +
                                    '<td><span class="badge" style="background-color:#19751A">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>'); 

                                } else if (subjecthistories[b][4] == '1.25') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' + '<td><span class="badge" style="background-color:#4CAF50">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '1.5') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#8BC349">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '1.75') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#CDDC39">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#FFCF4B">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.25') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#F9B32F">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.5') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' + '<td><span class="badge" style="background-color:#F39C12">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '2.75') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#E67E22">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] == '3.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#C86400">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');

                                } else if (subjecthistories[b][4] =='5.0') {
                                  $("#content").append('<tr>' +
                                  '<td>' + subjecthistories[b][3] + '</td>' +
                                  '<td>' + subjecthistories[b][6] + '</td>' +'<td><span class="badge" style="background-color:#ff0000">' + subjecthistories[b][4] + "0" + '</span>' + ' ' + '<i title="Grade is locked" class="fa fa-lock text-gray"></i> </td> </tr>');
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


function loadselecteddegree() {

}

function recommendation() {
  var varstudid = document.getElementsByClassName('bodyclass')[0].id;
  console.log("Load All Recommendation")
  $.ajax({
    url: "http://127.0.0.1:5000/engine",
    contentType: "application/json",
    type: "GET",
    dataType: "json",
    async: false,
    data: { "studid": String(varstudid) },

    success: function(resp) {
      if (resp.status == "ok") {
        // console.log(resp.data);
        for (i = 0; i < resp.count; i++) {
          programs = resp.data[resp.data.length - 1].programs;
          syandsem = resp.data[i].syandsem;
          passedsubjs = resp.data[i].passedsubjs;
          degreename = resp.data[i].DegreeName[0];
          specificcourses = resp.data[i].specific_courses.specific_subjects;
          currentsem = resp.data[i].specific_courses.current_sem;
          subjects = resp.data[i].subjects;
          total_units = resp.data[i].total_units;
          residency = resp.data[i].residency;

          for (let x = 0; x < programs.length; x++ ) {
            if (degreename == programs[x][0]) {

                    $("#recommendationcontainer").append('<p> <strong> Degree Name: <span style="color: red;">' + programs[x][0] + '</span>' + '&emsp;&emsp;' + 'Total Units: (<span style="color: red;">' + total_units + ' </span>) </strong></p>');

                    $("#recommendationcontainer").append('<table> <tr class="active"> <th width="100%"> Current Sem: ' + currentsem + '</th> </tr> </table>');

                    $("#recommendationcontainer").append('<table class="table table-bordered table-hover table-striped">' +
                      '<tr class="active"> <th width="3%"> SubjCode </th> <th width="25%"> Description </th> <th width="5%"> Pre-Requisite </th> <th width="5%"> Units </th> </tr>');

                    for(let a = 0; a < specificcourses.length; a++) {              
                          $("#recommendationcontainer").append('<tbody width="100%"> <tr>' +
                          '<td width="5%">' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + specificcourses[a].subjcode + '</td>' +
                          '<td width="24%">' + '&nbsp;' + specificcourses[a].subjdesc + '</td>' +
                          '<td width="8%">' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + specificcourses[a].prereq + '</td>' +
                          '<td width="5%">' + '&nbsp;' + specificcourses[a].unit + '</td> </tr> <tbody> </table>'); 
                      }

                      $("#recommendationcontainer").append('<br>');


                      for(let b = 0; b < syandsem.length; b++) {

                          if (syandsem[b].sem == 3) {
                            $("#recommendationcontainer").append('<tr>' + 
                                '<td colspan="3" class="danger"> <strong>' + "Year:  " + syandsem[b].year + "&emsp;" + " SEM: " + "Summer Sem" + '</strong> </td> </tr>');
                          } else {
                            $("#recommendationcontainer").append('<tr>' + 
                              '<td colspan="3" class="danger"> <strong>' + "Year:  " + syandsem[b].year + "&emsp;" + " SEM: " + syandsem[b].sem + '</strong> </td> </tr>');
                          }
                          

                          $("#recommendationcontainer").append('<table class="table table-bordered table-hover table-striped"> <tr class="active"> <th width="3%"> SubjCode </th> <th width="25%"> Description </th> <th width="5%"> Pre-Requisite </th> <th width="5%"> Units </th> </tr>');


                          for(let c=0; c < subjects.length; c++) {

                            if( (subjects[c].yeartotake==syandsem[b].year) && (subjects[c].semtotake==syandsem[b].sem) ) {

                                $("#recommendationcontainer").append('<tbody width="100%"> <tr width="100%">' +
                                '<td width="5%">' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + subjects[c].subjcode + '</td>' +
                                '<td width="24%">' + '&nbsp;' + subjects[c].subjdesc + '</td>' +
                                '<td width="8%">' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + subjects[c].prereq + '</td>' +
                                '<td width="5%">' + '&nbsp;' + subjects[c].unit + '</td> </tr> </tbody> </table>');

                            }
                          }
                          
                          $("#recommendationcontainer").append('<hr> <br>');

                      }


        //       // for (let d=0; d < gpas.length; d++) {
        //       //   if ((gpas[d].sy == syandsem[a][0] ) && (gpas[d].sem == syandsem[a][1] )) {
        //       //     $("#content").append('<tr>' +
        //       //                         '<td colspan="2" class="text-right text-danger">' + "GPA " + '</td>' +
        //       //                         '<td class="text-danger">' + gpas[d].gpa + '</td> </tr>');
        //       //   }
        //       // }
              
        //             // $("#content").append('<br><hr>');
          }
        }
        

        }

      
      } else {
          $("#recommendationcontainer").html("");
      }
    },

    error: function(e) {
      alert("danger! Something went wrong!");
      console.log(e)
    }

  });
  
}

function loadrecommendation() {
  home();
  recommendation();
}


function loadhome() {
  home();
}

function loadacademicperformance() {
  home();
  academicperformance();
}

function loadstudentinfo() {
  studentinformation();
}

function loadadviseme() {
  
}