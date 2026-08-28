package pe.edu.upeu.orden.controller;

import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.orden.entity.Orden;
import pe.edu.upeu.orden.service.OrdenService;
import java.util.List;

@RestController
@RequestMapping("/api/ordenes")
public class OrdenController {
    private final OrdenService service;
    public OrdenController(OrdenService service) { this.service = service; }
    @GetMapping
    public List<Orden> listar() { return service.listar(); }
    @PostMapping
    public Orden crear(@RequestBody Orden orden) { return service.guardar(orden); }
    @GetMapping("/{id}")
    public Orden buscar(@PathVariable Long id) { return service.buscarPorId(id); }
    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id) { service.eliminar(id); }
}
