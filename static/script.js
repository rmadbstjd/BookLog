// 페이지마다 공용으로 쓰일만한 js 코드를 넣습니다.
function render_nav(nickname) {
  let nav_html = `<div class="topbtn mb-5">
        <a>${nickname}님</a>
        <button
          type="button"
          class="btn btn-secondary"
          onclick="window.location.href = '/login'"
        >
          로그인
        </button>
        <button
          type="button"
          class="btn btn-secondary"
          onclick="window.location.href = '/register'"
        >
          회원가입
        </button>
      </div>`;

  $("#nav").append(nav_html);
}
