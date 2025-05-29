# Copyright (C) 2017 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com, author Milian Wolff <milian.wolff@kdab.com>
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from bs4 import BeautifulSoup
from PySide6.QtCore import QObject, Signal, Slot


class Core(QObject):
    """An instance of this class gets published over the WebChannel and is then
       accessible to HTML clients."""
    sendText = Signal(str)
    receivedText = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def _emit_send_text(self, text):
        self.sendText.emit(text)

    @Slot(str)
    def receiveText(self, text):
        # remove any html tags and weird spaces
        text = BeautifulSoup(text, "html.parser").get_text().strip()
        self.receivedText.emit(text)
