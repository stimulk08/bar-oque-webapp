function isValidDate(d) {
    return d instanceof Date && !isNaN(d);
}

function isGreaterThanCurrentDate(d) {
    let currentDate = new Date();
    return currentDate <= d;
}

function rjust(number) {
    return ("00" + number.toString()).slice(-2);
}

function convertDateToStr(d) {
    return `${d.getFullYear()}-${rjust(d.getMonth() + 1)}-${rjust(d.getDate())}`
}

let chosenTime, lastTimeBtn, chosenTable, chosenDate, chosenDuration, clientName;

$(document).ready(function () {
    let $loadTimes = $("#loadAvailableTimes");
    $loadTimes.toggle();

    $(".btn_table").click(function (event) {
        let target = event.target;
        let tableNumber = $(target).data("table-number");
        chosenTable = tableNumber;
        $("#modal_reservation_title").text("Забронировать столик " + tableNumber);
    });

    let $alertErrors = $("#alert_errors_for_pick_time");
    let maxYear = 2022;
    $("#form_for_pick_time").submit(function (event) {
        event.preventDefault();
        $alertErrors.css("display", "none");
        let $dateInput = $("#pick_date");
        let currentDate = new Date($dateInput.val());

        if (!isValidDate(currentDate)) {
            $alertErrors.html("Неверный формат даты. Правильный: 01.01.2021")
            $alertErrors.css("display", "block");
            return
        }

        if (!isGreaterThanCurrentDate(currentDate)) {
            $alertErrors.html("Пожалуйста, выберете дату не меньшую сегодняшней")
            $alertErrors.css("display", "block");
            return
        }

        if (currentDate.getFullYear() > maxYear) {
            $alertErrors.html("Слишком далекий год. Пожалуйста, выберете год не больше, чем " + maxYear);
            $alertErrors.css("display", "block");
            return
        }

        chosenDate = convertDateToStr(currentDate);
        chosenDuration = $("#select_duration").val();
        let data = {
            date: chosenDate,
            duration: chosenDuration,
            table: chosenTable
        }
        $.ajax({
            url: getAvailableTimesUrl,
            type: "GET",
            data: data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function () {
                $loadTimes.toggle();
            }
        }).done(function (res, textStatus, jqXHR) {
            if (jqXHR.readyState === 4 && jqXHR.status === 200) {
                addAvailableTimes(res.times);
                $loadTimes.toggle();
                $("#block_name").css("display", "block");
            }
        }).fail(function () {
            $loadTimes.toggle();
        });
    });

    let $btnMakeReservation = $("#btn_make_reservation");
    let $inputName = $("#input_name");
    $inputName.change(function () {
        $btnMakeReservation.prop("disabled", false);
    });

    $btnMakeReservation.click(function () {
        clientName = $inputName.val();
        let $sendProcess = $("#send_process");
        let data = `table_id=${chosenTable}&client_name=${clientName}&date=${chosenDate}&time=${chosenTime}&duration=${chosenDuration}`;
        let $btnSubmitReservation = $("#btn_submit_reservation");
        $.ajax({
            url: createReservationUrl,
            type: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            data: data,
            beforeSend: function (){
                $sendProcess.toggle();
            }
        }).done(function (res, textStatus, jqXHR) {
            if (jqXHR.readyState === 4 && jqXHR.status === 201) {
                $("#qr").attr("src", res.qr_code);
                let fileName = res.date + "_" + res.time + "_столик_" + chosenTable + ".png"
                $("#btn_download_qr").attr("href", res.qr_code).attr("download", fileName);
                $("#success_alert").html("Вы успешно забронировали столик: " + chosenTable);
                $("#success_reservation_block").css("display", "block");
                $btnSubmitReservation.removeClass("btn-danger");
                $btnSubmitReservation.addClass("btn-success");
                $btnSubmitReservation.html("Отлично");
                $("#modal_pick_time").modal("hide");
                $("#modal_result_reservation").modal("show");
                $sendProcess.toggle();
            }
        }).fail(function () {
            let $failedReservationBlock = $("#failed_reservation_block");
            $failedReservationBlock.html("Не удалось забронировать столик. Пожалуйста, сообщите нам об ошибке");
            $failedReservationBlock.css("display", "block");
            $btnSubmitReservation.removeClass("btn-success");
            $btnSubmitReservation.addClass("btn-danger");
            $btnSubmitReservation.html("Мы вам сообщим");
            $("#modal_pick_time").modal("hide");
            $("#modal_result_reservation").modal("show");
            $sendProcess.toggle();
        });
    });
});

function addAvailableTimes(availableTimes) {
    let $timesBlock = $("#available_times");
    $timesBlock.empty();
    availableTimes.forEach(e => {
        let btnTime = $(
            `<button class="btn btn-outline-dark fw-bolder fs-5" data-time="${e}">${e}</button>`
        )
        btnTime.click(function (e) {
            let btn = $(e.target);
            if (lastTimeBtn !== undefined) {
                lastTimeBtn.removeClass("btn-dark");
                lastTimeBtn.addClass("btn-outline-dark");
            }
            btn.removeClass("btn-outline-dark");
            btn.addClass("btn-dark");
            lastTimeBtn = btn;
            chosenTime = btn.data("time");
        })
        $timesBlock.append(btnTime);
    });
}