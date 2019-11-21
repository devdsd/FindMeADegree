function academic_performance(){
    $.ajax({
        url: 'http://localhost:5000/academic_performance/',
        type: "GET",
        dataType: "json",
        success: function (resp) {
            $("#acadperf").html("Hello");
            if (resp.status == 'ok') {
                // for (i = 0; i < resp.count; i++) {
                //     bh_id = resp.entries[i].bh_id;
                //     bh_name = resp.entries[i].bh_name;
                //     address = resp.entries[i].address;
                //     accommodation_type = resp.entries[i].accommodation_type;
                //     allowed_gender = resp.entries[i].allowed_gender;
                //     contact_no = resp.entries[i].contact_no;
                //     vacancy = resp.entries[i].vacancy;
                //     rent_rate = resp.entries[i].rent_rate;
                //     bh_owner_id = resp.entries[i].bh_owner_id;

                //     $("#boardinghouses").append(showbhinfo(bh_id, bh_name,
                //         address, accommodation_type, allowed_gender, contact_no, vacancy, rent_rate,
                //         bh_owner_id));
                alert(resp);
                // }

            } else {
                $("#acadperf").html("Hello");
                alert("Wala!");
            }
        },
        error: function (e) {
            alert("danger!");
        }

    });
}