/**
 * 1. OFFLINE MULTI-LINGUAL DICTIONARY MATRIX
 */
const translations = {
    en: {
        home: "Home",
        users: "Users",
        profile: "Profile",
        logout: "Logout",
        feed_title: "Your Feed",
        create_btn: "+ Create New Post",
        like: "Like",
        liked: "Liked",
        comments: "Comments",
        send: "Send",
        write_comment: "Write a comment...",
        discover: "Discover Members",
        view_profile: "View Profile",
        follow: "Follow",
        unfollow: "Unfollow",
        edit_profile: "Edit Basic Profile",
        save_bio: "Save Bio",
        delete: "Delete"
    },
    ta: {
        home: "முகப்பு",
        users: "பயனர்கள்",
        profile: "சுயவிவரம்",
        logout: "வெளியேறு",
        feed_title: "உங்கள் பதிவுவரிசை",
        create_btn: "+ புதிய பதிவு",
        like: "விருப்பு",
        liked: "விருப்பம் தெரிவிக்கப்பட்டது",
        comments: "கருத்துகள்",
        send: "அனுப்பு",
        write_comment: "உங்கள் கருத்தை எழுதுங்கள்...",
        discover: "உறுப்பினர்களைக் கண்டறியவும்",
        view_profile: "சுயவிவரம் பார்",
        follow: "பின்தொடர்",
        unfollow: "விலகு",
        edit_profile: "சுயவிவரத்தை மாற்று",
        save_bio: "பயோ சேமி",
        delete: "நீக்கு"
    }
};

/**
 * 2. RUN LANGUAGE SWITCHER ENGINE
 */
function changeLanguage(lang) {
    // Save selection locally so choice survives tab navigation checks
    localStorage.setItem("selectedLanguage", lang);
    
    // Find all nodes tagged with our translate marker attribute properties
    document.querySelectorAll("[data-translate]").forEach(element => {
        const key = element.getAttribute("data-translate");
        if (translations[lang] && translations[lang][key]) {
            // Safely swap value strings instantly without forcing whole page reload ticks
            if (element.tagName === "INPUT" && element.placeholder) {
                element.placeholder = translations[lang][key];
            } else {
                element.innerText = translations[lang][key];
            }
        }
    });
}

// Ensure the chosen language persists when navigating between pages
document.addEventListener("DOMContentLoaded", () => {
    const savedLang = localStorage.getItem("selectedLanguage") || "en";
    const dropdown = document.getElementById("langDropdown");
    if (dropdown) {
        dropdown.value = savedLang;
    }
    changeLanguage(savedLang);
});

/**
 * 3. Collapsible Comments Tray Toggle
 */
function toggleComments(postId) {
    const tray = document.getElementById(`comments-tray-${postId}`);
    if (tray) {
        tray.style.display = tray.style.display === "none" ? "block" : "none";
    }
}

/**
 * 4. Post Deletion Confirmation Hook
 */
function confirmDelete(event) {
    const userAgreed = confirm("Are you sure you want to permanently delete this post?");
    if (!userAgreed) {
        event.preventDefault();
        return false;
    }
    return true;
}

/**
 * 5. Profile Bio Drawer Switcher
 */
function toggleEditProfileForm() {
    const drawer = document.getElementById("edit-profile-drawer");
    const toggleBtn = document.getElementById("edit-profile-toggle-btn");
    if (drawer) {
        if (drawer.style.display === "none") {
            drawer.style.display = "block";
            if (toggleBtn) toggleBtn.innerText = "Hide Edit Panel";
        } else {
            drawer.style.display = "none";
            if (toggleBtn) toggleBtn.innerText = "Edit Basic Profile";
        }
    }
}
