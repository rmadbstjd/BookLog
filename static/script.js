// 페이지마다 공용으로 쓰일만한 js 코드를 넣습니다.

function render_nav(nickname, title) {
  let nav_html = `<nav class="navbar bg-light justify-content-md-center" id="nav">
      <div class="container-fluid p-3 px-5">
        <a class="navbar-brand text-dark" href='/'>Booklog</a>
        <ul class="nav justify-content-end">
          <li class="nav-item">
            <a class="nav-link active text-dark" id="for_control_1" aria-current="page" href="/login">로그인</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-dark"id="for_control_2" href='/register'>회원가입</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-dark disabled is-hidden" id="nickname"></a>
            <a class="nav-link text-dark is-hidden">로그아웃</a>
          </li>
        </ul>
      </div>
      </nav>

      <div class="jumbotron p-5 p-md-5 text-white rounded bg-info">
        <div class="col-md-8 px-0">
          <h1 class="display-4 font-italic">${title}</h1>
          <p class="lead my-3">책을 읽고 느낀 것들을 공유하는 공간 - 
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ut dolor corrupti consequuntur!</p> 

        </div>
      </div>
      `;

  $("#header_above").append(nav_html);
}

function addNickname() {
  $.ajax({
    type: "POST",
    url: "/index/addnick",
    data: {},
    success: function (nick) {
      $("#nickname").text(nick["nick"] + " 님");
    },
  });
}
function hidebtn() {
  if (document.cookie != "") {
    console.log("로그인이 되어있습니다.");
    $("#for_control_1").toggleClass("is-hidden");
    $("#for_control_2").toggleClass("is-hidden");
  } else {
    console.log("로그인이 되어있지 않습니다.");
    $("#nickname").toggleClass("nickname");
  }
}
