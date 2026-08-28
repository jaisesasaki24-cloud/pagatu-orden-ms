package pe.edu.upeu.orden.service;

import org.springframework.stereotype.Service;
import pe.edu.upeu.orden.entity.Orden;
import pe.edu.upeu.orden.repository.OrdenRepository;
import java.util.List;

@Service
public class OrdenService {
    private final OrdenRepository repository;
    public OrdenService(OrdenRepository repository) { this.repository = repository; }
    public List<Orden> listar() { return repository.findAll(); }
    public Orden guardar(Orden orden) { return repository.save(orden); }
    public Orden buscarPorId(Long id) { return repository.findById(id).orElse(null); }
    public void eliminar(Long id) { repository.deleteById(id); }
}
