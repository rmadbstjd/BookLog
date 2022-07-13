// 페이지마다 공용으로 쓰일만한 js 코드를 넣습니다.

function render_nav(nickname) {
  let nav_html = `      <div class="container-fluid">
        <a class="navbar-brand" href="#">Booklog</a>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <a class="nav-link" href="/login">로그인</a>
            <a class="nav-link" href='/register'>회원가입</a>
            <a class="nav-link disabled" id="nickname">${nickname} 님</a>
          </div>
        </div>
      </div>`;

  $("#nav").append(nav_html);
}
