import qrcode

# Ссылка на GitHub-репозиторий
github_url = "https://github.com/nkt50i/cylinder"
qr1 = qrcode.make(github_url)
qr1.save("qr_github.png")

# Ссылка на публикацию или источник
paper_url = "https://repository.kpfu.ru/?p_id=231822"
qr2 = qrcode.make(paper_url)
qr2.save("qr_paper.png")
