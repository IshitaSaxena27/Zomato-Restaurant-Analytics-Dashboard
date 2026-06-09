console.log("AI Restaurant Intelligence Platform Loaded");

document.addEventListener(
    "DOMContentLoaded",
    function(){

        console.log(
            "Dashboard Ready"
        );

        const cards =
        document.querySelectorAll(
            ".kpi-card"
        );

        cards.forEach(
            (card,index)=>{

                card.style.opacity=0;

                card.style.transform=
                "translateY(30px)";

                setTimeout(()=>{

                    card.style.transition=
                    "0.6s";

                    card.style.opacity=1;

                    card.style.transform=
                    "translateY(0px)";

                },index*150);

            }
        );

        const charts =
        document.querySelectorAll(
            ".chart-box"
        );

        charts.forEach(
            chart=>{

                chart.addEventListener(
                    "mouseenter",
                    function(){

                        chart.style.transform=
                        "scale(1.02)";

                    }
                );

                chart.addEventListener(
                    "mouseleave",
                    function(){

                        chart.style.transform=
                        "scale(1)";

                    }
                );

            }
        );

    }
);