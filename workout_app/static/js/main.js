// Display the toast notification when the page is loaded
window.addEventListener("DOMContentLoaded", function () {
  // Select all elements with class 'toast' and convert the NodeList to an array
  var toastElList = [].slice.call(document.querySelectorAll(".toast"));

  // Create an array of bootstrap.Toast instances based on the selected elements
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl);
  });

  // Show each toast notification in the array
  toastList.forEach(function (toast) {
    toast.show();
  });
});
