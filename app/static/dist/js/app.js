function showsemstudent(studid, sem, sy, studlevel, scholasticstatus, scholarstatus, studmajor, gpa, cgpa) {
  return (
    '<div class="col-lg-12">' +
    "<h2>" +
    studid +
    "&nbsp;&nbsp;" +
    sem +
    "</h2>" +
    "<p> <h4> School Year: </h4>" +
    sy +
    "</br> <h4>Student Level: </h4>" +
    studlevel +
    "</br> <h4>Scholastic Status: </h4>" +
    scholasticstatus +
    "</br> <h4>Scholarship Status: </h4>" +
    scholarstatus +
    "</br> " +
    "<h4>Student Major: </h4>" +
    studmajor +
    "</br> <h4>GPA: </h4>" +
    gpa +
    "</br> <h4>CGPA: </h4>" +
    cgpa +
    "</p> </div>"
  );
}


function showsemstudenttoggle() {
  $.ajax({
    url: "http://127.0.0.1:5000/sampleapi",
    contentType: "application/json",
    type: "GET",
    dataType: "json",

    success: function(resp) {
      $("#sampleapi").html("");
      if (resp.status == "ok") {
        for (i = 0; i < resp.count; i++) {
          studid = resp.entries[i].studid;
          sem = resp.entries[i].sem;
          sy = resp.entries[i].sy;
          studlevel = resp.entries[i].studlevel;
          scholasticstatus = resp.entries[i].scholasticstatus;
          scholarstatus = resp.entries[i].scholarstatus;
          studmajor = resp.entries[i].studmajor;
          gpa = resp.entries[i].gpa;
          cgpa = resp.entries[i].cgpa;

          $("#sampleapi").append(
            showsemstudent( studid, sem, sy, studlevel, scholasticstatus, scholarstatus, studmajor, gpa, cgpa )
          );
        }
      } else {
        $("#sampleapi").html("");
        alert(resp.message);
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
        $("#block").html("");
        alert("Sorry");
      }
    },

    error: function(e) {
      alert("danger! Something went wrong!");
    }
  });
}


// function showacademicperformance() {
//   return(
//     <div class="box">

//     <div class="table-responsive">

//         <div class="box-" style="padding: 15px;">

//             <p> <strong> Cummulative GPA: <span style="color: red;"> {{ cgpa }} </span> </strong> </p>

//             <table class="table table-bordered table-hover table-striped">
//                 <tbody>
//                     <tr class="active">
//                         <th width="3%"> SubjCode </th>
//                         <th width="25%"> Description </th>
//                         <th width="5%"> Grade </th>
//                     </tr>

//                     {% for sysem in syandsem %}
//                         {% if sysem.sem is none %}
//                             <p> Wala </p>
//                         {% elif (sysem.sem == '3') %}
//                             <tr>
//                                 <td colspan="3" class="danger"> <strong> SY: {{ sysem.sy }} SEM: Summer Sem </strong> ( <span
//                                         class="text-muted" style="text-transform: uppercase;"> {{ semstudent.studmajor }}:
//                                         {{ student_program.progdesc }} </span>) </td>
//                             </tr>
//                         {% else %}
//                             <tr>
//                                 <td colspan="3" class="danger"> <strong> SY: {{ sysem.sy }} SEM: {{ sysem.sem }} </strong> ( <span
//                                         class="text-muted" style="text-transform: uppercase;"> {{ semstudent.studmajor }}:
//                                         {{ student_program.progdesc }} </span>) </td>
//                             </tr>
//                         {% endif %}

//                         {% for subjhistory in subjecthistories %}
//                             {% if (subjhistory.sy == sysem.sy) and (subjhistory.sem == sysem.sem) %}

//                             <tr id="2014-20151COMPSCI1N">
//                                 <td> {{ subjhistory.subjcode }} </td>
//                                 <td> {{ subjhistory.subjdesc }} </td>

//                                 {% if (subjhistory.grade == '1.0') %}
//                                 <td><span class="badge" style="background-color:#19751A"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '1.25') %}
//                                 <td><span class="badge" style="background-color:#4CAF50"> {{ subjhistory.grade }} </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '1.5') %}
//                                 <td><span class="badge" style="background-color:#8BC349"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '1.75') %}
//                                 <td><span class="badge" style="background-color:#CDDC39"> {{ subjhistory.grade }} </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '2.0') %}
//                                 <td><span class="badge" style="background-color:#FFCF4B"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '2.25') %}
//                                 <td><span class="badge" style="background-color:#F9B32F"> {{ subjhistory.grade }} </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '2.5') %}
//                                 <td><span class="badge" style="background-color:#F39C12"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '2.75') %}
//                                 <td><span class="badge" style="background-color:#E67E22"> {{ subjhistory.grade }} </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '3.0') %}
//                                 <td><span class="badge" style="background-color:#C86400"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% elif (subjhistory.grade == '5.0') %}
//                                 <td><span class="badge" style="background-color:#ff0000"> {{ subjhistory.grade }}0 </span> <i
//                                         title="Grade is locked" class="fa fa-lock text-gray"></i> </td>
//                                 {% endif %}
//                             </tr>

//                             {% endif %}
//                         {% endfor %}


//                         {% for gpa in gpas %}
//                             {% if (gpa.sy == sysem.sy ) and (gpa.sem == sysem.sem )  %}
//                             <tr>
//                                 <td colspan="2" class="text-right text-danger">GPA</td>
//                                 <td class="text-danger"> {{ gpa.gpa }} </td>
//                             </tr>
//                             {% endif %}
//                         {% endfor %}

//                     {% endfor %}


//                 </tbody> <!-- tbody end -->
//             </table>

//         </div>

//     </div>
// </div>
//   );
// }


function academicperformance() {
  $.ajax({
    url: "http://127.0.0.1:5000/academic_performance",
    contentType: "application/json",
    type: "GET",
    dataType: "json",

    success: function(resp) {
      if (resp.status == "ok") {
        for (i = 0; i < resp.count; i++) {

          res.append({"cgpa": float(cgpa), "syandsem": syandsem, "studmajor": str(latestsemstud.studmajor), "studentprogram": str(student_program.progdesc), "subjecthistories": subjecthistories, "gpas": gpas})

          cgpa = resp.data[i].cgpa;
          syandsem = resp.data[i].syandsem;
          studmajor = resp.data[i].studmajor;
          studentprogram = resp.data[i].studentprogram;
          subjecthistories = resp.data[i].subjecthistories;

          
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
        $("#block").html("");
        alert("Sorry");
      }
    },

    error: function(e) {
      alert("danger! Something went wrong!");
    }
  });
}

