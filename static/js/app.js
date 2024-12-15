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

  const CorrectButtons = document.querySelectorAll("button#correct-btn");

  const CorrectsCounter = document.querySelectorAll("input#corrects-counter");

  CorrectButtons.forEach((button, index) => {
    button.addEventListener("click", function () {
      const answerId = parseInt(CorrectsCounter[index].dataset.answerId, 10);

      const request = new Request(`/answerLike/${answerId}`, {
        method: "post",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
      });

      fetch(request)
        .then((response) => response.json())
        .then((data) => {
          const counter = CorrectsCounter[index];
          counter.value = data.likesCount;
        });
    });
  });

  const correctCheckboxes = document.querySelectorAll("input.form-check-input");

  correctCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const answerId = parseInt(checkbox.dataset.answerId, 10);

      const request = new Request(`/correct/${answerId}`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
      });

      fetch(request)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.isCorrect) {
            checkbox.checked = true;
          } else {
            checkbox.checked = false;
          }
        });
    });
  });
};

init();
