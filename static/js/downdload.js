var loading_HTML = '<div class="loading"><div class="bars-common bar-one"></div><div class="bars-common bar-two"></div><div class="bars-common bar-three"></div><div class="squares-common square-one"></div><div class="squares-common square-two"></div></div>'
var stop_icon = '<svg t="1672116503404" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="8099" width="16" height="16"><path d="M310.1 904.2c-33.8 0-61.2-27.4-61.2-61.2V181.4c0-33.8 27.4-61.2 61.2-61.2 33.8 0 61.2 27.4 61.2 61.2V843c0 33.8-27.4 61.2-61.2 61.2zM713.5 904.2c-33.8 0-61.2-27.4-61.2-61.2V181.4c0-33.8 27.4-61.2 61.2-61.2 33.8 0 61.2 27.4 61.2 61.2V843c0.1 33.8-27.3 61.2-61.2 61.2z" fill="#13227a" p-id="8100"></path></svg>'
var start_icon = '<svg t="1672116139611" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7832" width="16" height="16"><path d="M899.117 526.883a30.04 30.04 0 0 1-3.976 5.365 29.922 29.922 0 0 1-1.548 1.58l-0.2 0.186a30.087 30.087 0 0 1-5.472 4.057L165.858 955.094c-0.047 0.027-0.1 0.046-0.143 0.073q-1.155 0.659-2.37 1.214c-0.145 0.066-0.289 0.132-0.434 0.2q-1.084 0.476-2.212 0.864c-0.238 0.083-0.475 0.165-0.713 0.241-0.645 0.205-1.3 0.386-1.963 0.548-0.348 0.085-0.7 0.168-1.044 0.24-0.56 0.116-1.126 0.213-1.7 0.3q-1.416 0.21-2.833 0.283h-0.016a29.977 29.977 0 0 1-4.5-0.107c-0.243-0.024-0.483-0.057-0.723-0.086a30.513 30.513 0 0 1-2.109-0.331 31.377 31.377 0 0 1-1.021-0.222c-0.6-0.139-1.191-0.293-1.78-0.469-0.331-0.1-0.658-0.2-0.984-0.315q-0.921-0.309-1.82-0.676c-0.241-0.1-0.479-0.2-0.716-0.307q-1.047-0.461-2.055-1c-0.108-0.058-0.215-0.118-0.322-0.177a29.753 29.753 0 0 1-8.652-7.174l-0.071-0.089a29.873 29.873 0 0 1-1.59-2.124c-0.3-0.439-0.589-0.885-0.866-1.34-0.108-0.179-0.233-0.341-0.338-0.524a29.859 29.859 0 0 1-4-16V95.886a30 30 0 0 1 44.981-26.984l722.265 417a30 30 0 0 1 10.988 40.981zM180.89 877.13l632.327-365.2L180.89 146.856V877.13z" fill="#13227a" p-id="7833"></path></svg>'

window.addEventListener('pywebviewready', function () {
    console.log('pywebview is ready now!');
})

function delete_tr(c_title) {
    var _tr = event.srcElement;
    _tr.parentElement.parentElement.remove()
    console.log("删除 " + _tr.parentElement.parentElement.getAttribute("id"))

    var td0s = document.getElementsByClassName(c_title+"td-0")
    for (var td0 = 0; td0 < td0s.length; td0++) {
        td0s[td0].innerHTML = td0 + 1
    }

    pywebview.api.delete_tr(_tr.parentElement.parentElement.getAttribute("id"))
}

function explore_tr() {
    var _tr = event.srcElement;

    pywebview.api.explore_tr(_tr.parentElement.parentElement.getAttribute("id"))
}