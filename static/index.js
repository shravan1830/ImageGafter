const LOCALHOST = "http://127.0.0.1:5000"

document.onkeydown = function (e) {
    if (e.key === "F12") {
        e.preventDefault();
    }
};

// Prevent right-click 
document.addEventListener("contextmenu", function (e) {
    e.preventDefault();
});



const get_path = async (image_file_path, n_images) =>
{

    if(image_file_path != null && n_images > 0)
        {
            req= await fetch(`${LOCALHOST}/set_path`,
                {
                    headers:{
                        'Content-Type': 'application/json',
                    },
                    method:"POST",
                    body:JSON.stringify({image_file_path,n_images})
                }
            )
            if (req["status"] == 200)
                window.location.href = req["url"]
    
        }

    

}
const graftBtn = document.getElementById('graft_btn')
graftBtn.addEventListener('click', async function  (event) {

    file_path = document.getElementById("image_path").value
    n_images = document.getElementById("n_images").value

  res = await get_path(file_path, n_images)
  console.log(res)

})