//---------------------------------------------------------
function key(left, name, note, clazz) {
	var html = ""
    html +="<div class='" + clazz + "' "
    html +=     "style='left:" + left + ";' " 
    html +=     "onmousedown='midi_key_down(" + note + ")' " 
    html +=     "onmouseup='midi_key_up(" + note + ")' " 
    html +=     "></div>"

    return html
}

//---------------------------------------------------------
function key_black(left, name, note) { return key(left, name, note, "key_black") }

//---------------------------------------------------------
function key_white(left, name, note) { return key(left, name, note, "key_white") }

//---------------------------------------------------------
function build_keys() {
    var html = ""
    html += key_white(100, "C3", 60)
    html += key_white(140, "D3", 62)
    html += key_white(180, "E3", 64)
    html += key_white(220, "F3", 65)
    html += key_white(260, "G3", 67)
    html += key_white(300, "A4", 69)
    html += key_white(340, "B4", 71)
    
    html += key_white(380, "C4", 72)
    html += key_white(420, "D4", 74)
    html += key_white(460, "E4", 76)
    html += key_white(500, "F4", 77)
    html += key_white(540, "G4", 79)
    html += key_white(580, "A5", 81)
    html += key_white(620, "B5", 83)
    
    html += key_black(120, "C#3", 61)
    html += key_black(160, "D#3", 63)
    html += key_black(240, "F#3", 66)
    html += key_black(280, "G#3", 68)
    html += key_black(320, "A#4", 70)
    
    html += key_black(400, "C#4", 73)
    html += key_black(440, "D#4", 75)
    html += key_black(520, "F#4", 78)
    html += key_black(560, "G#4", 80)
    html += key_black(600, "A#5", 82)

    var div = $("#keys").get(0)
    div.innerHTML = html
}

