var loading_HTML = '<div class="loading"><div class="bars-common bar-one"></div><div class="bars-common bar-two"></div><div class="bars-common bar-three"></div><div class="squares-common square-one"></div><div class="squares-common square-two"></div></div>'
var detail_loading = '<div class="bg"><svg onclick="ask_download()"t="1671846005666"class="d_icon"viewBox="0 0 1024 1024"version="1.1"xmlns="http://www.w3.org/2000/svg"p-id="5288"width="32"height="32"><path d="M96 896h832c17.673 0 32 14.327 32 32 0 17.673-14.327 32-32 32H96c-17.673 0-32-14.327-32-32 0-17.673 14.327-32 32-32z m448.906-132.192l276.45-276.45c12.497-12.496 32.758-12.496 45.255 0 12.497 12.497 12.497 32.759 0 45.255L535.597 863.627c-12.497 12.497-32.758 12.497-45.255 0L148.546 524.483c-12.497-12.496-12.497-32.758 0-45.254 12.496-12.497 32.758-12.497 45.254 0l287.106 284.453 0.032-667.427c0-17.673 14.327-32 32-32 17.673 0 32 14.327 32 32l-0.032 667.553z"p-id="5289"fill="#1296db"></path></svg><svg onclick="close_detail()"t="1671845148532"class="x_icon"viewBox="0 0 1024 1024"version="1.1"xmlns="http://www.w3.org/2000/svg"p-id="2678"width="32"height="32"><path d="M507.168 473.232L716.48 263.936a16 16 0 0 1 22.624 0l11.312 11.312a16 16 0 0 1 0 22.624L541.12 507.168 750.4 716.48a16 16 0 0 1 0 22.624l-11.312 11.312a16 16 0 0 1-22.624 0L507.168 541.12 297.872 750.4a16 16 0 0 1-22.624 0l-11.312-11.312a16 16 0 0 1 0-22.624l209.296-209.312-209.296-209.296a16 16 0 0 1 0-22.624l11.312-11.312a16 16 0 0 1 22.624 0l209.296 209.296z"fill="#1296db"p-id="2679"></path></svg><div class="loading"><div class="bars-common bar-one"></div><div class="bars-common bar-two"></div><div class="bars-common bar-three"></div><div class="squares-common square-one"></div><div class="squares-common square-two"></div></div></div>'


window.addEventListener('pywebviewready', function () {
    console.log('pywebview is ready now!');
    pywebview.api.first_loading().then(res=>{
        var card_p = document.getElementsByClassName("plane")[0];
        card_p.innerHTML = res[0];
        document.getElementById('total_pg').innerHTML = res[1];
    })

})

// function keyDown(event) {
//     pywebview.api.p(event.keyCode);
//     pywebview.api.full_screen(event.keyCode);
// }
// document.onkeydown = keyDown
function go_video_index() {
    var div = event.srcElement;
    // document.getElementById('1');
    // event.srcElement;
    var detail_panel = document.getElementsByClassName('detail_panel')[0]
    while (div.className != 'card') {
        div = div.parentNode;
    }
    var vid = div.getAttribute('id');
    console.log(vid);

    detail_panel.innerHTML = detail_loading
    detail_panel.style.display = 'block'

    pywebview.api.get_video_id(vid).then(res=>{
        detail_panel.innerHTML = res

    })
}

function set_api() {
    var api = event.srcElement;
    var api_text = document.getElementsByClassName("v_api_text")[0];
    api_text.textContent = api.textContent
    // pywebview.api.set_api();

}

function set_class() {
    var api = event.srcElement;
    var api_text = document.getElementsByClassName("v_class_text")[0];
    var card_p = document.getElementsByClassName("plane")[0];
    var t_pg = document.getElementById('total_pg')
    api_text.textContent = api.textContent
    card_p.innerHTML = loading_HTML;
    document.getElementById("now_pg").innerHTML = '第1页'
    pywebview.api.get_class_info("天空资源", api_text.textContent, 1).then(res => {
        card_p.innerHTML = res[0];
        console.log(res[0])
        t_pg.innerHTML = res[1]
    });


}

function show_his() {
    var his_p = document.getElementsByClassName('his_panel')[0];
    his_p.style.visibility = 'visible'
}

function close_his() {
    var his_p = document.getElementsByClassName('his_panel')[0];
    his_p.style.visibility = 'hidden';
}

function clear_his() {

    var his_cards = document.getElementsByClassName('his_cards')[0];
    his_cards.innerHTML = ''

}

function go_pg(pg) {
    var this_pg = document.getElementById("now_pg");
    var my_pg = document.getElementById("my_pg");
    var card_plane = document.getElementsByClassName("plane")[0];

    card_plane.innerHTML = loading_HTML
    pywebview.api.go_pg(pg).then(res => {
        this_pg.innerHTML = res['now_pg'];
        card_plane.innerHTML = res['cards'];
    })

}

function close_detail(){
    var dp = document.getElementsByClassName('detail_panel')[0]
    dp.style.display = 'none'
}

function close_detail_by_mask(){
    var dp = document.getElementsByClassName('detail_panel')[0]
    var clicked_div = event.srcElement
    if (clicked_div.className == 'detail_panel'){
        dp.style.display = 'none'
    }
}

function play(_from, _url){
    pywebview.api.play(_from, _url).then(res=>{
        console.log(res)
    })
}

function ask_download(){
    console.log('ask for download page')
}

function search(_type){
    var card_p = document.getElementsByClassName("plane")[0];
    var t_pg = document.getElementById('total_pg')
    var input_box = document.getElementById("search")

    card_p.innerHTML = loading_HTML
    if(_type == 0){
        pywebview.api.search_this(input_box.value).then(res=>{
            input_box.value = ''
            card_p.innerHTML = res[0];
            t_pg.innerHTML = res[1]
        })
    }else{
        pywebview.api.search_all(input_box.value).then(res=>{
            input_box.value = ''
            card_p.innerHTML = res[0];
            t_pg.innerHTML = res[1]
        })
    }
}

function open_dl_panel(){
    pywebview.api.open_dl_panel()
}

