//---------------------------------------------------------
function midi_xhr_success(data, text_status) {
//  alert("xhr_success: data='" + data + "'; text_status='" + text_status + "'")
}

//---------------------------------------------------------
function midi_xhr_error(xhr, text_status, error_thrown) {
    alert("xhr_error: text_status='" + text_status + "'; error_thrown='" + error_thrown + "'")
}

//---------------------------------------------------------
function midi_send_message(message) {
    var data = JSON.stringify(message, null, 4)
    
    return $.ajax({
        type: "POST",
        url: "io",
        contentType: "text/json",
        processData: false,
        data: data,
        success: midi_xhr_success,
        error: midi_xhr_error
    })
}

//---------------------------------------------------------
function midi_key_down(note) {
    var message = {
        NoteOn: {
            channel:  0,
            key:      note,
            velocity: 127
        }
    }
    
    return midi_send_message(message)
}

//---------------------------------------------------------
function midi_key_up(note) {
    var message = {
        NoteOff: {
            channel:  0,
            key:      note,
            velocity: 127
        }
    }
    
    return midi_send_message(message)
}

//---------------------------------------------------------
function midi_control_change(note) {
    var message = {
        ControlChange: {
            channel:    0,
            controller: controller,
            value:      value
        }
    }
    
    return midi_send_message(message)
}