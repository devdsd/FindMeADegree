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


function studfname(studfirstname) {
  return (studfirstname);
}

function studfname2(studlastname) {
  return (studlastname);
}

function studfnameandlname(studfirstname, studlastname) {
  return (studfirstname + " " + studlastname);
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
          
          // alert(studfirstname)
          $("#studname").append(
            studfname(studfirstname)
          );
          $("#studname2").append(
            studfname2(studfirstname)
          );
          $("#firstandlastname").append(
            studfnameandlname(studfirstname, studlastname)
          );
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

