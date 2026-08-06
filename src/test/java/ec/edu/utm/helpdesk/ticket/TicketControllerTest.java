package ec.edu.utm.helpdesk.ticket;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@WithMockUser
class TicketControllerTest {
    @Autowired MockMvc mvc;

    private static final String TICKET = """
        {"titulo":"Sin conexión","descripcion":"No hay acceso a Internet","categoria":"RED","prioridad":"ALTA","estado":"ABIERTO"}
        """;

    @Test void crudCompleto() throws Exception {
        String location = mvc.perform(post("/tickets").contentType(MediaType.APPLICATION_JSON).content(TICKET))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.id").isNumber())
                .andReturn().getResponse().getHeader("Location");
        mvc.perform(get(location)).andExpect(status().isOk()).andExpect(jsonPath("$.titulo").value("Sin conexión"));
        mvc.perform(get("/tickets")).andExpect(status().isOk()).andExpect(jsonPath("$[0].categoria").value("RED"));
        mvc.perform(put(location).contentType(MediaType.APPLICATION_JSON).content(TICKET.replace("ABIERTO", "CERRADO")))
                .andExpect(status().isOk()).andExpect(jsonPath("$.estado").value("CERRADO"));
        mvc.perform(delete(location)).andExpect(status().isNoContent());
        mvc.perform(get(location)).andExpect(status().isNotFound());
    }

    @Test void rechazaDatosInvalidos() throws Exception {
        mvc.perform(post("/tickets").contentType(MediaType.APPLICATION_JSON).content("{}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.errores.titulo").exists());
    }

    @Test void requiereAutenticacion() throws Exception {
        mvc.perform(get("/tickets").with(org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.anonymous()))
                .andExpect(status().isUnauthorized());
    }
}
