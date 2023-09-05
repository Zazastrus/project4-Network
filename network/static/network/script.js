document.addEventListener("DOMContentLoaded", function() {

    document.getElementsByName('edit').forEach(button => {

        button.onclick = () => {

            const id = button.value;
            
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
                document.getElementById(`edit_div_${id}`).style.display = "none";

                if (document.getElementById(`anchor_${id}`)){
                    document.getElementById(`anchor_${id}`).innerHTML = newCont;
                }
                else {
                    // This is for Profile Page
                    document.getElementById(`h6_${id}`).innerHTML = newCont;
                }
                document.getElementById(`post_${id}`).style.display = "block";
            };
            return false;
        }
    });

    document.getElementsByName("like").forEach(button => {

        button.onclick = () => {
            
            const id = button.value;
            fetch(`post/${id}`)
            .then(response => response.json())
            .then(post => {
                const past_like = post["like"];
                const new_like = past_like + 1;
                console.log(post)
                fetch(`post/${id}`,{
                    method: "PUT",
                    body: JSON.stringify({
                        like: new_like
                    })
                })
                document.getElementById(`like_${id}`).innerHTML = `&#10084; ${new_like}`;
                document.getElementById(`div_like_${id}`).style.display = "none";
                document.getElementById(`div_dislike_${id}`).style.display = "block";
            });
        };
        return false;
    });

    document.getElementsByName("dislike").forEach(button => {

        button.onclick = () => {
            
            const id = button.value;
            fetch(`post/${id}`)
            .then(response => response.json())
            .then(post => {
                const past_like = post["like"];
                const new_like = past_like - 1;

                fetch(`post/${id}`,{
                    method: "PUT",
                    body: JSON.stringify({
                        like: new_like
                    })
                })
                document.getElementById(`like_${id}`).innerHTML = `&#10084; ${new_like}`;
                document.getElementById(`div_like_${id}`).style.display = "block";
                document.getElementById(`div_dislike_${id}`).style.display = "none";
            });
        };
        return false;
    });

});