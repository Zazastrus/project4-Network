document.addEventListener("DOMContentLoaded", function() {

    document.getElementsByName('edit').forEach(button => {

        button.onclick = () => {

            const id = button.value;
            console.log(id);
            document.getElementById(`edit_div_${id}`).style.display = "block";
            document.getElementById(`post_${id}`).style.display = "none";

            document.getElementById(`save_${id}`).onclick = () => {
                const newCont = document.getElementById(`post_edit_${id}`).value;

                // PUT, Update the post's content
                fetch(`post/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: newCont
                    })
                })
                this.location.reload()
            }
        }
    });

    document.getElementsByName("like").forEach(button => {

        button.onclick = () => {
            
            console.log(button.value)
            fetch(`post/${button.value}`)
            .then(response => response.json())
            .then(post => {
                const past_like = post["like"];
                const new_like = past_like + 1;
                console.log(post)
                fetch(`post/${button.value}`,{
                    method: "PUT",
                    body: JSON.stringify({
                        like: new_like
                    })
                })
                this.location.reload()
            });
        };
    });

    document.getElementsByName("dislike").forEach(button => {

        button.onclick = () => {

            fetch(`post/${button.value}`)
            .then(response => response.json())
            .then(post => {
                const past_like = post["like"];
                const new_like = past_like - 1;

                fetch(`post/${button.value}`,{
                    method: "PUT",
                    body: JSON.stringify({
                        like: new_like
                    })
                })
                this.location.reload()
            })
        }
    })
});