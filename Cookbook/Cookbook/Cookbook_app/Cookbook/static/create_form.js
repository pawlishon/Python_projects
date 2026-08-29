if (!document.querySelector('.search-form')) {
    const main = document.querySelector("main")
    var search_form = document.createElement("form")
    search_form.classList.add('search-form')
    search_form.setAttribute("method", "get")
    search_form.setAttribute("class", "search-form")
    search_form.setAttribute("action", "/search")
    search_form.innerHTML = '<label for="Title">Tytuł:</label><br><input type="text" id="title" name="title"><br>' +
        '<label for="categorylist">Kategorie:</label><br>' +
        '<select name="categorylist">' +
        '<option>Dowolna</option>' +
        '<option>dania glowne miesne</option>' +
        '<option>makarony i ryz</option>' +
        '<option>przystawki</option>' +
        '<option>dania glowne inne</option>' +
        '<option>wypieki wytrawne</option>' +
        '<option>dania glowne wege</option>' +
        '<option>sosy wytrawne</option>' +
        '<option>sniadanie</option>' +
        '<option>przekaski</option>' +
        '<option>zupy</option>' +
        '<option>desery</option>' +
        '<option>sosy dipy slodkie</option>' +
        '<option>wypieki slodkie</option>' +
        '<option>jedzenie dla niemowlat</option>' +
        '<option>napoje</option>' +
        '<option>dodatki</option>' +
        '<option>dania glowne rybne</option>' +
        '<option>przepisy podstawowe</option>' +
        '<option>pieczywo</option></select><br>' +
        '<br><input type="submit" value="Szukaj" id="submit_conditions" style= "color:black">'
    main.prepend(search_form)
}
