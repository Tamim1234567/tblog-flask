var typed = new Typed("#element", {
    strings: ["Web developer", "Web designer", "programmer"],
    typeSpeed: 120,
  });
  
  function toggleShow() {
    document.getElementById("show-nav").style.display = "none";
    document.getElementById("logo").style.display = "none";
    document.getElementById("hide-nav").style.display = "block";
    document.getElementById("hide-on-sm").style.display = "flex";
    document.querySelector("nav").style.flexDirection = "column";
    document.querySelector("nav").style.position = "abselute";
  }
  function toggleHide() {
    let x = window.matchMedia("(max-width: 900px)");
    if (x.matches) {
      document.getElementById("show-nav").style.display = "block";
      document.getElementById("logo").style.display = "block";
      document.getElementById("hide-nav").style.display = "none";
      document.getElementById("hide-on-sm").style.display = "none";
      document.querySelector("nav").style.flexDirection = "row";
      document.querySelector("nav").style.position = "fixed";
    } else {
      console.log("not mobile");
    }
  }
  window.addEventListener(
    "scroll",
    () => {
      document.body.style.setProperty(
        "--scroll",
        window.pageYOffset / (document.body.offsetHeight - window.innerHeight)
      );
    },
    false
  );