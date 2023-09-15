from functions import *

passwd = "pueaeaqvjnszeffv"
sender = "docswapza@gmail.com"

recipients = [
    "docswapza@gmail.com",
]


subject = "We have found a SwapGroup for you!"
n_swap = 5
ref_number = 12345

body = f"""<html>
            <body>
                <p>It's your lucky day 🎉</p>

                <p>We have found a <strong>{n_swap}-way swap</strong> for your internship placement! You can find their email(s) in the recipients section of this mail.</p>

                <p>So what's next?</p>
                <ul>
                    <li>You should get in touch with each other and coordinate your swap; it's probably best to do this with a group chat. If you have more than a 2-way swap, a diagram will be attached to this mail to guide you on who needs to swap with who.</li>
                    <li>Notify your hospitals of the swap.</li>
                    <li>Tell your friends about DocSwap!</li>
                </ul>

                <p>🚨 Some important things to consider</p>
                <ul>
                    <li>Due to the nature of multiway swaps, they will <strong>ONLY</strong> work if everyone is onboard. If one of you backs out, the chain will be broken, and the swap will no longer work!</li>
                    <li>If this happens to your SwapGroup, you should re-apply on <a href="https://docswap.streamlit.app/">DocSwap</a> so that we can find you another SwapGroup.</li>
                    <li>If you are not happy with your SwapGroup, you should notify them ASAP so that everyone can re-apply</li>
                    <li>Some people don't check their emails; don't sit around waiting forever. If someone in your SwapGroup hasn't responded to any of your emails, you should notify them one last time that you are backing out of the swap and re-applying for a different SwapGroup.</li>
                </ul>

                <p>If you have any questions or feedback, please submit it on <a href="https://forms.gle/kW8PFEtboYf3JiKS6">this form</a> with the reference number: <strong>{ref_number}</strong></p>
            </body>
            </html>
            """

send_email(sender, passwd, recipients, subject, body, attachment_path="demo_swap.png")
