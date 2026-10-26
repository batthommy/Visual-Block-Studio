if (is_logged_in && user) {
    const setInfo = (id, label, value) => {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = `${label}: ${value}`;
        }
    };

    const formatTime = (minutes) => {
        const total = Math.max(0, Number(minutes) || 0);
        const hours = Math.floor(total / 60);
        const mins = Math.floor(total % 60);

        if (hours === 0) return `${mins}m`;
        if (mins === 0) return `${hours}h`;

        return `${hours}h ${mins}m`;
    };

    const formatSeconds = (seconds) => {
        const total = Math.max(0, Math.floor(Number(seconds) || 0));
        const hours = Math.floor(total / 3600);
        const minutes = Math.floor((total % 3600) / 60);
        const secs = total % 60;

        if (hours > 0) return `${hours}h ${minutes}m ${secs}s`;
        if (minutes > 0) return `${minutes}m ${secs}s`;

        return `${secs}s`;
    };

    setInfo("menu-logged-in-name", "NAME", user.name);
    setInfo("menu-logged-in-project", "PROJECTS", user.projects.length);
    setInfo("menu-logged-in-friends", "FRIENDS", user.friends ?? 0);
    setInfo("menu-logged-in-people-followed", "FOLLOWING", user.peoplefollowed ?? 0);
    setInfo("menu-logged-in-total-time", "TOTAL TIME", formatTime(user.totaltime_mnt));
    setInfo("menu-logged-in-program-time", "CODING TIME", formatTime(user.programtime_mnt));
    setInfo("menu-logged-in-best-longest-time", "LONGEST SESSION", formatSeconds(user.bestlongesttime_sec));
}