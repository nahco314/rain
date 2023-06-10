from abc import ABC

from rain.generator import Generator


class PreProcessorGenerator(Generator, ABC):
    @property
    def if_true(self) -> bytes:
        return b"#if'%s'<'%s'\n" % (self.null, self.question)

    @property
    def if_false(self) -> bytes:
        return b"#if'%s'<'%s'\n" % (self.null, self.null)

    @property
    def end_if(self) -> bytes:
        return b"#endif\n"
