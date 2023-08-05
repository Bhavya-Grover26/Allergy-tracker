const MobileMenu = {
    open() {
      document.querySelector("aside").classList.add("active");
    },
    close() {
      document.querySelector("aside").classList.remove("active");
    },
  };
  
  const Modal = {
    index : 0,
    getindex(){
      return this.index;
    },
    open() {
      document.getElementById("modalOverlay").classList.add("active");
    },
    edit(ind){
      document.getElementById("modalOverlayEdit").classList.add("active");
      this.index = ind;
      FormEdit.setFields(ind);
    },
    close() {
      document.getElementById("modalOverlay").classList.remove("active");
      Form.clearFields();
    },
    editclose(){
      document.getElementById("modalOverlayEdit").classList.remove("active");
      Form.clearFields();
    },
  };
  
  
  // Display date (November, 24)
  let today = new Date();
  let dd = String(today.getDate()).padStart(2, "0");
  let mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!;
  let yyyy = today.getFullYear();
  today = dd + "/" + mm + "/" + yyyy;
  
  let myDate;
  function formatDate(str) {
    var parts = str.split("/").map(Number);
    myDate = new Date("20" + parts[2], parts[1] - 1, parts[0]);
    return myDate.toLocaleString([], { month: "long" });
  }
  myDate = today;
  const dateDisplay = formatDate(myDate.toString()) + ", " + dd;
  
  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
  
  document.getElementById("date-display").innerHTML =
    capitalizeFirstLetter(dateDisplay);