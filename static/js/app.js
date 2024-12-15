function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

const init = () => {
  const LikeButtons = document.querySelectorAll("button#like-btn");

  const LikesCounter = document.querySelectorAll("input#likes-counter");

  LikeButtons.forEach((button, index) => {
    button.addEventListener("click", function () {
      const questionId = parseInt(LikesCounter[index].dataset.questionId, 10);

      const request = new Request(`/like/${questionId}`, {
        method: "post",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
      });

      fetch(request)
        .then((response) => response.json())
        .then((data) => {
          const counter = LikesCounter[index];
          counter.value = data.likesCount;
        });
    });
  });
};

init();
