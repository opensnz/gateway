/********************** ready **************************/

$( document ).ready(function() {
    $.each($('select'), function () {
        $(this).selectmenu({ width : $(this).attr("width")})
    });
    currentUI();
});

$('#tabs').tabs({
    create: function( event, ui ) {
        applyCamera();
    },
    activate: function(event, ui){
        // index 0 equals to Camera Tab
        if(ui.newTab.index() == 0){
            applyCamera();
        }
    }
});

$( "#button-icon-disk" ).button({
	icon: "ui-icon-disk",
	showLabel: false
}).click(function(){
    window.location.href = '/explorer';
});

$( "#button-icon-info" ).button({
	icon: "ui-icon-info",
	showLabel: false
}).click(function(){
    window.location.href = '/about';
});

$( ".button-default" ).button({
	icon: "ui-icon-gear",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/default",
        type: "POST",
        datatype: "json",
        success: function(data){
            applyTelemetry(data);
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});

/********************** tabs-1 **************************/

// enable camera
$("#enableCamera").change(function() {
    enable = false;
    if(this.checked){
        enable = true;
    }
    $.ajax({
        url: "/api/camera/state",
        type: "POST",
        data: {"state" : enable},
        datatype: "json",
        success: function(data){
            if(data['state'] == true) {
                $("#enableCamera").prop( "checked", true );
            }else if(data['state'] == false){
                $("#enableCamera").prop( "checked", false );
            }else{
                $("#enableCamera").prop( "checked", !enable );
                showError('400');
            }
        },
        error: function(xhr){
            $("#enableCamera").prop( "checked", !enable );
            showError(xhr.status);
        },
    });
});

// enable intruder
$("#enableIntruder").change(function() {
    enable = false;
    if(this.checked){
        enable = true;
    }
    $.ajax({
        url: "/api/camera/intruder",
        type: "POST",
        data: {"intruder" : enable},
        datatype: "json",
        success: function(data){
            if(data['intruder'] == true) {
                $("#enableIntruder").prop( "checked", true );
            }else if(data['intruder'] == false){
                $("#enableIntruder").prop( "checked", false );
            }else{
                $("#enableIntruder").prop( "checked", !enable );
                showError('400');
            }
        },
        error: function(xhr){
            $("#enableIntruder").prop( "checked", !enable );
            showError(xhr.status);
        },
    });
});

// record duration 
$("#duration").selectmenu({
    change: function( event, data ) {
        $.ajax({
            url: "/api/telemetry/duration",
            type: "POST",
            data: {"duration" : data.item.value},
            datatype: "json",
            success: function(data){
                if(data['duration'] != null) {
                    $('#duration  option[value="60"]').prop("selected", true);
                }else{
                    showError('400');
                }
            },
            error: function(xhr){
                showError(xhr.status);
            },
        });
    }
});

/********************** tabs-2 **************************/

// kernel blur
$( "#button-kernel-minus" ).button({
	icon: "ui-icon-minusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/kernel_blur",
        type: "POST",
        data: {"operation" : -1},
        datatype: "json",
        success: function(data){
            $( "#kernel-blur" ).text(data['kernel_blur']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});
$( "#button-kernel-plus" ).button({
	icon: "ui-icon-plusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/kernel_blur",
        type: "POST",
        data: {"operation" : +1},
        datatype: "json",
        success: function(data){
            $( "#kernel-blur" ).text(data['kernel_blur']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});

// mask threshold
$( "#button-mask-minus" ).button({
	icon: "ui-icon-minusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/mask_threshold",
        type: "POST",
        data: {"operation" : -1},
        datatype: "json",
        success: function(data){
            $( "#mask-threshold" ).text(data['mask_threshold']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});
$( "#button-mask-plus" ).button({
	icon: "ui-icon-plusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/mask_threshold",
        type: "POST",
        data: {"operation" : +1},
        datatype: "json",
        success: function(data){
            $( "#mask-threshold" ).text(data['mask_threshold']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});

/********************** tabs-3 **************************/

// surface step
$( "#button-surface-step-minus" ).button({
	icon: "ui-icon-minusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/surface_step",
        type: "POST",
        data: {"operation" : -1},
        datatype: "json",
        success: function(data){
            $( "#surface-step" ).text(data['surface_step']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});
$( "#button-surface-step-plus" ).button({
	icon: "ui-icon-plusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/surface_step",
        type: "POST",
        data: {"operation" : +1},
        datatype: "json",
        success: function(data){
            $( "#surface-step" ).text(data['surface_step']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});

// surface threshold
$( "#button-surface-threshold-minus" ).button({
	icon: "ui-icon-minusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/surface_threshold",
        type: "POST",
        data: {"operation" : -1},
        datatype: "json",
        success: function(data){
            $( "#surface-threshold" ).text(data['surface_threshold']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});
$( "#button-surface-threshold-plus" ).button({
	icon: "ui-icon-plusthick",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/surface_threshold",
        type: "POST",
        data: {"operation" : +1},
        datatype: "json",
        success: function(data){
            $( "#surface-threshold" ).text(data['surface_threshold']);
            $("#enableCamera").prop( "checked", true );
            $("#enableIntruder").prop( "checked", false );
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});

/********************** tabs-4 **************************/

/********************** Not Implemented **************************/







// alert error
function showError(status){
    var statusErrorMap = {
        '400' : "Bad Request",
        '401' : "Unauthorized",
        '403' : "Forbidden",
        '404' : "Not Found",
        '405' : "Method Not Allowed",
        '408' : "Request Timeout",
        '500' : "Internal Server Error",
        '501' : "Not Implemented",
        '503' : "Service unavailable"
    };
    message =statusErrorMap[status];
    if(!message){
        message="Unknown Error";
    }
    alert(message);
}