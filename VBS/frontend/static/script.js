//!! JS still to be done !!

/* 
    !! Like linking numbers and projects to actual sources, variables, and arrays, 
    !! tweaking a few things, fixing button connections, etc.
*/

if (is_logged_in) {
    console.log("Utente autenticato");
}
if (is_logged_in) {
    console.log(user.id);
    console.log(user.name);
    console.log(user.username);
    console.log(user.email);
    console.log(user.age);
    console.log(user.birthdate);
    console.log(user.description);
    console.log(user.created_at);
    console.log(user.projects);
}
if (is_logged_in) {
    user.projects.forEach(project => {
        console.log(project.name);
    });
}