def formatar_saida(state):
    linhas = []

    for email in state["emails"]:
        emoji = {
            "ALTA": "🔴",
            "MÉDIA": "🟡",
            "BAIXA": "🟢"
        }.get(email["urgency"], "⚪")

        linhas.append("📧 NOVO EMAIL")
        linhas.append(f"De: {email['from']}")
        linhas.append(f"Assunto: {email['subject']}")
        linhas.append(f"Urgência: {emoji} {email['urgency']}")

        if email["suggestion"]:
            linhas.append("\n💡 Sugestão de resposta:")
            linhas.append(email["suggestion"])

        linhas.append("-" * 50)

    if state["events"]:
        linhas.append("📅 EVENTOS PRÓXIMOS")
        for ev in state["events"]:
            local = "💻 Online" if ev["is_online"] else f"📍 {ev['location']}"
            linhas.append(f"• {ev['subject']} — {ev['start']} ({local})")

    return "\n".join(linhas)
