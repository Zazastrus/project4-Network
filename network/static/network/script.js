document.addEventListener("DOMContentLoaded", function() {

    document.getElementsByName('edit').forEach(button => {

        button.onclick = () => {

            const id = button.value;
            
            document.getElementById(`edit_div_${id}`).style.display = "block";
            document.getElementById(`post_${id}`).style.display = "none";

            // The SAVE button only works when the text area isn't empty.
            const saveButton = document.getElementById(`save_${id}`);
            const editArea = document.getElementById(`post_edit_${id}`);
            saveButton.disabled = true;
            editArea.onkeyup = () => {
                if (editArea.value.length > 0){
                    saveButton.disabled = false;
                }
                else {
                    saveButton.disabled = true;
                }
            }

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

    document.getElementsByName(`followAct`).forEach(button => {
        button.onclick = () => {
            const profile = button.value;
            const act = button.innerHTML;
            const count = parseInt(document.getElementById('followers').innerHTML);
            
            if (act === 'Follow'){
                fetch(`${profile}`,{
                    method: 'POST',
                    body: JSON.stringify({
                        f: act
                    })
                });
                let newCount = count + 1;
                document.getElementById('follow').style.display = 'none';
                document.getElementById('unfollow').style.display = 'block';
                document.getElementById('followers').innerHTML = newCount;
                return false;
            }
            else {
                fetch(`${profile}`,{
                    method: 'POST',
                    body: JSON.stringify({
                        f: act
                    })
                })
                let newCount = count - 1;
                document.getElementById('follow').style.display = 'block';
                document.getElementById('unfollow').style.display = 'none';
                document.getElementById('followers').innerHTML = newCount;
                return false;
            }
        };
    });

    // The POST button only work when the text area isn't empty
    const postButton = document.getElementById('post_button');
    const postArea = document.getElementById('post_area');

    if (postButton){
        postButton.disabled = true;

        postArea.onkeyup = () => {
            if (postArea.value.length > 0){
                postButton.disabled = false;
            }
            else {
                postButton.disabled = true;
            }
        }
    }
    

    const commentButton = document.getElementById('comment_button');
    const commentArea = document.getElementById('comment_area');
    
    if (commentButton){
        commentButton.disabled = true;
        
        commentArea.onkeyup = () => {
            if (commentArea.value.length > 0){
                commentButton.disabled = false;
            }
            else {
                commentButton.disabled = true;
            }
        }
    }
    
});