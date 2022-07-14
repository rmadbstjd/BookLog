(function (factory) {
  if (typeof define === "function" && define.amd) {
    define(["jquery"], factory);
  } else if (typeof exports === "object") {
    factory(require("jquery"));
  } else {
    factory(jQuery);
  }
})(function ($) {
  var pluses = /\+/g;
  function encode(s) {
    return config.raw ? s : encodeURIComponent(s);
  }
  function decode(s) {
    return config.raw ? s : decodeURIComponent(s);
  }
  function stringifyCookieValue(value) {
    return encode(config.json ? JSON.stringify(value) : String(value));
  }
  function parseCookieValue(s) {
    if (s.indexOf('"') === 0) {
      s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\");
    }
    try {
      s = decodeURIComponent(s.replace(pluses, " "));
      return config.json ? JSON.parse(s) : s;
    } catch (e) {}
  }
  function read(s, converter) {
    var value = config.raw ? s : parseCookieValue(s);
    return $.isFunction(converter) ? converter(value) : value;
  }
  var config = ($.cookie = function (key, value, options) {
    if (arguments.length > 1 && !$.isFunction(value)) {
      options = $.extend({}, config.defaults, options);

      if (typeof options.expires === "number") {
        var days = options.expires,
          t = (options.expires = new Date());
        t.setTime(+t + days * 864e5);
      }
      return (document.cookie = [
        encode(key),
        "=",
        stringifyCookieValue(value),
        options.expires ? "; expires=" + options.expires.toUTCString() : "", // use expires attribute, max-age is not supported by IE
        options.path ? "; path=" + options.path : "",
        options.domain ? "; domain=" + options.domain : "",
        options.secure ? "; secure" : "",
      ].join(""));
    }

    var result = key ? undefined : {};

    var cookies = document.cookie ? document.cookie.split("; ") : [];

    for (var i = 0, l = cookies.length; i < l; i++) {
      var parts = cookies[i].split("=");
      var name = decode(parts.shift());
      var cookie = parts.join("=");

      if (key && key === name) {
        result = read(cookie, value);
        break;
      }

      if (!key && (cookie = read(cookie)) !== undefined) {
        result[name] = cookie;
      }
    }

    return result;
  });

  config.defaults = {};

  $.removeCookie = function (key, options) {
    if ($.cookie(key) === undefined) {
      return false;
    }

    $.cookie(key, "", $.extend({}, options, { expires: -1 }));
    return !$.cookie(key);
  };
});

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
            <a class="nav-link text-dark disabled" id="nickname"></a>
            <a class="nav-link text-dark" id="logout" onclick="click_logout()">로그아웃</a>
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

function click_logout() {
  $.removeCookie = function (key, options) {
    if ($.cookie(key) === undefined) {
      return false;
    }

    $.cookie(key, "", $.extend({}, options, { expires: -1 }));
    return !$.cookie(key);
  };
  $.removeCookie("mytoken", { path: "/" });
  alert("로그아웃이 되었습니다.");

  window.location.href = "/";
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
    //로그인이 되었습니다.
    $("#for_control_1").hide();
    $("#for_control_2").hide();
    console.log("됏다");
    addNickname();
  } else {
    //로그인이 안 되었습니다.
    console.log("안됏다");
    $("#nickname").hide();
    $("#logout").hide();
  }
}
